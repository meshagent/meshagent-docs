import asyncio
import logging
from meshagent.api.room_server_client import TextDataType
from meshagent.agents import ToolResponseAdapter
from meshagent.tools import Tool, Toolkit, ToolContext
from meshagent.api.messaging import FileResponse, JsonResponse, TextResponse
from meshagent.api.services import ServiceHost
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.openai.tools.responses_adapter import WebSearchTool
from meshagent.agents.llmrunner import LLMTaskRunner
from meshagent.otel import otel_config
from meshagent.agents.agent import AgentCallContext
from meshagent.tools.storage import StorageToolkit


otel_config(service_name="resume-runner")
log = logging.getLogger("resume-runner")
log.setLevel(logging.DEBUG)
logging.getLogger("meshagent").setLevel(logging.DEBUG)
logging.getLogger("openai_agent").setLevel(logging.DEBUG)  # LLM adapter
logging.getLogger("httpx").setLevel(logging.INFO)          # bump to DEBUG for wire traces

service = ServiceHost() 

# replace with storage toolkit
# class GetResume(Tool):
#     def __init__(self):
#         super().__init__(
#             name="get-resume",
#             title="get-resume",
#             description="A tool that returns a resume from file storage",
#             input_schema={
#                 "type": "object",
#                 "additionalProperties": False,
#                 "required": ["resume_path"],
#                 "properties": {
#                     "resume_path": {"type": "string"}
#                 }
#             }
#         )
#     async def execute(self, context:ToolContext, resume_path: str):
#         resume = await context.room.storage.download(path=resume_path)
#         return FileResponse(data=resume.data, name=resume.name, mime_type=resume.mime_type)

class SaveCandidateDetails(Tool):
    def __init__(self):
        super().__init__(
            name="save-candidate-details",
            title="save-candidate-details",
            description="Store information about a candidate in the room database",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["resume_path", "candidate_name", "contact_info", "resume_text", "resume_summary", "web_search_notes"],
                "properties": {
                    "resume_path": {"type": "string"},
                    "candidate_name": {"type": "string"},
                    "contact_info": {"type": "string"},
                    "resume_text": {"type": "string"},
                    "resume_summary": {"type": "string"},
                    "web_search_notes": {"type":"string"}
                }
            }
        )
    async def execute(self, context:ToolContext, resume_path:str, candidate_name:str, contact_info:str|None, resume_text:str, resume_summary:str, web_search_notes:str|None):
        record = {
                    "resume_path": resume_path,
                    "candidate_name": candidate_name,
                    "contact_info": contact_info,
                    "resume_text": resume_text,
                    "resume_summary": resume_summary, 
                    "web_search_notes": web_search_notes
                }
        try:
            await context.room.database.insert(table="candidates", records=[record])
        except Exception as e:
            return JsonResponse(json={"status":"error", "error":str(e), "resume_path":resume_path})
        return JsonResponse(json={"status":"ok", "saved":record})

resume_toolkit = Toolkit(name="resume-tools", tools=[WebSearchTool(), SaveCandidateDetails()])

# Resume agent needs to take in a file, process the file, save the file and results to the room
# Agent should compare the resume to other job descriptions and indicate if the person is a match for them
@service.path(identity="resume-runner", path="/resumerunner")
class ResumeRunner(LLMTaskRunner):
    def __init__(self):
        super().__init__(
            name="resume-runner",
            title="resume-runner",
            description="A TaskRunner that processes Resumes",
            llm_adapter=OpenAIResponsesAdapter(),
            supports_tools=True,
            toolkits=[resume_toolkit, StorageToolkit()],
            # input_schema={"prompt":""},
            rules=[
                "You process resumes to determine if candidates are a good fit for open roles",
                "When invoked, you MUST first call the get-resume tool with the provided resume_path to obtain the resume file.",
                "Next extract the person's name, contact information, skills, and a concise experience summary",
                "Once you have extracted skills from their resume, look them up on LinkedIn and Google to see if you can find additional information about the candidate",
                "Once you have collected enough information about the candidate, save their information to the candidate database using the save-candidate-details tool"
            ]
        )
    async def start(self, *, room):
        await super().start(room=room)
        log.info("creating tables if they do not exist")
        await room.database.create_table_with_schema(
            name="candidates",
            schema={
                "resume_path": TextDataType(),
                "candidate_name": TextDataType(),
                "contact_info": TextDataType(),
                "resume_text": TextDataType(),
                "resume_summary": TextDataType(), 
                "web_search_notes": TextDataType()
            },
            mode="create_if_not_exists"
        )
        log.info("finished creating tables")

    # Override ask to avoid duplicating toolkits (context.toolkits already contains self._toolkits)
    async def ask(self, *, context: AgentCallContext, arguments: dict):
        prompt = arguments.get("prompt")
        if prompt is None:
            raise ValueError("`prompt` is required")

        context.chat.append_user_message(prompt)

        resp = await self._llm_adapter.next(
            context=context.chat,
            room=context.room,
            toolkits=context.toolkits,  # already includes this agent's toolkits need to fix potential bug in LLMRunner
            tool_adapter=self._tool_adapter,
            output_schema=self.output_schema,
        )

        if self.output_schema is None:
            return TextResponse(text=resp)
        return resp

asyncio.run(service.run())
# meshagent agents ask --room=resume --agent=resume-runner --input='{"prompt": "Process this resume: with resume_path ParsaResume.pdf"}'