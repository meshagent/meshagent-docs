import asyncio
import logging
import uuid
import os
from meshagent.api import RequiredToolkit
from meshagent.api.room_server_client import TextDataType
from meshagent.agents import ToolResponseAdapter
from meshagent.tools import Tool, Toolkit, ToolContext, RemoteToolkit
from meshagent.api.messaging import FileResponse, JsonResponse, TextResponse
from meshagent.api.services import ServiceHost
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.openai.tools.responses_adapter import WebSearchTool
from meshagent.agents.llmrunner import LLMTaskRunner
from meshagent.otel import otel_config
from meshagent.agents.agent import AgentCallContext
from meshagent.tools.storage import StorageToolkit
from meshagent.agents.mail import MailWorker

otel_config(service_name="resume-runner")
log = logging.getLogger("resume-runner")
log.setLevel(logging.DEBUG) # switch to info later 

service = ServiceHost() 

class SaveCandidateDetails(Tool):
    def __init__(self):
        super().__init__(
            name="save-candidate-details",
            title="save-candidate-details",
            description="Store information about a candidate in the room database",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["resume_path", "candidate_name", "contact_info", "resume_summary", "web_search_notes"],
                "properties": {
                    "resume_path": {"type": "string"},
                    "candidate_name": {"type": "string"},
                    "contact_info": {"type": "string"},
                    "resume_summary": {"type": "string"},
                    "web_search_notes": {"type":"string"}
                }
            }
        )
    async def execute(self, context:ToolContext, resume_path:str, candidate_name:str, contact_info:str|None, resume_summary:str, web_search_notes:str|None):
        candidate_id = str(uuid.uuid4())
        record = {
                    "candidate_id": candidate_id,
                    "resume_path": resume_path,
                    "candidate_name": candidate_name,
                    "contact_info": contact_info,
                    "resume_summary": resume_summary, 
                    "web_search_notes": web_search_notes
                }
        try:
            await context.room.database.insert(table="candidates", records=[record])
        except Exception as e:
            return JsonResponse(json={"status":"error", "error":str(e), "resume_path":resume_path})
        return JsonResponse(json={"status":"ok", "saved":record})

class SaveJobDescriptionDetails(Tool):
    def __init__(self):
        super().__init__(
            name="save-job-description-details",
            title="save-job-description-details",
            description="Store information about open roles and their job description in the room database",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["hiring_manager", "job_title", "job_description_path", "required_skills"],
                "properties": {
                    "hiring_manager": {"type": "string"},
                    "job_title": {"type": "string"},
                    "job_description_path": {"type": "string"},
                    "required_skills": {"type": "string"}
                }
            }
        )
          
    async def execute(self, context:ToolContext, hiring_manager:str, job_title:str, job_description_path:str, required_skills:str|None):
        role_id = str(uuid.uuid4())
        record = {
                    "role_id": role_id,
                    "hiring_manager": hiring_manager,
                    "job_title": job_title,
                    "job_description_path": job_description_path,
                    "required_skills": required_skills
                }
        try:
            await context.room.database.insert(table="open_roles", records=[record])
        except Exception as e:
            return JsonResponse(json={"status":"error", "error":str(e), "job_description_path":job_description_path})
        return JsonResponse(json={"status":"ok", "saved":record})
    
@service.path(identity="resume-toolkit", path="/resume-toolkit")
class ResumeToolkit(RemoteToolkit):
    def __init__(self):
        super().__init__(
            name="resume-toolkit",
            title="resume-toolkit",
            description="a toolkit for processing resumes and job descriptions",
            tools=[
                # *StorageToolkit().tools,
                # WebSearchTool(),
                SaveCandidateDetails(), 
                #SaveJobDescriptionDetails()
            ],
        )

# Tool for Mailbot to trigger the resume processing
class ProcessResume(Tool):
    def __init__(self):
        super().__init__(
            name="process-resume",
            title="process-resume",
            description="Copy a resume attachment from an email into the resumes folder for processing",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["attachment_path", "candidate_name", "candidate_email"],
                "properties": {
                    "attachment_path": {
                        "type": "string",
                        "description": "Path to the attachment saved by the mailworker (for example .emails/2025/01/01/12/00/00/abc123/attachments/resume.pdf)",
                    },
                    "candidate_name": {"type": "string"},
                    "candidate_email": {"type": "string"},
                },
            },
        )

    async def execute(
        self,
        context: ToolContext,
        attachment_path: str,
        candidate_name: str | None = None,
        candidate_email: str | None = None,
    ):
        # MailWorker saves attachments into .emails/.../attachments/<file>. Copy that into resumes/<file>
        filename = os.path.basename(attachment_path.rstrip("/"))
        target_path = f"resumes/{filename}"

        try:
            log.info(f"Saving resume to resumes/{target_path}")
            download = await context.room.storage.download(path=attachment_path)
            data = download.data
            handle = await context.room.storage.open(path=target_path, overwrite=True)
            try:
                await context.room.storage.write(handle=handle, data=data)
            finally:
                await context.room.storage.close(handle=handle)
        except Exception as e:
            return JsonResponse(
                json={
                    "status": "error",
                    "error": f"Failed to copy resume: {e}",
                    "attachment_path": attachment_path,
                }
            )
        
        # Invoke the TaskRunner to process the resume
        DEFAULT_RESUME_PROMPT = f"Process the candidate resume located at: {target_path}. You must extract the candidate's name and contact information from their resume and generate a succinct summary of their skills and experience. You can also use the web search tool to look for additional information about the candidate. Beware that some candidates may have common names and so it may be more difficult for you to find information about them. Once you have collected sufficient information about the candidate, store their information using the SaveCandidateDetails tool."

        resume_processing_prompt = os.getenv("") or DEFAULT_RESUME_PROMPT
        log.info(f"Processing resume with prompt: {resume_processing_prompt}")

        response = await context.room.agents.ask(
            agent="meshagent.runner",
            arguments={"prompt":resume_processing_prompt, "model":"gpt-5.2", "tools":[{"name":"storage"}, {"name":"web_search"}]},
            requires=[
                RequiredToolkit(name="resume-toolkit", tools=["save-candidate-details"])
            ]
        )

        log.info(f"TaskRunner Processing Response: {response}")

        return JsonResponse(
            json={
                "status": "ok",
                "resume_path": target_path,
                "candidate_name": candidate_name,
                "candidate_email": candidate_email,
            }
        )

@service.path(identity="mailbot-toolkit", path="/mailbot-toolkit")
class MailbotToolkit(RemoteToolkit):
    def __init__(self):
        super().__init__(
            name="mailbot-toolkit",
            title="mailbot-toolkit",
            description="A Toolkit for the MailWorker to kickoff resume processing",
            tools=[
                ProcessResume()
            ],
        )

# resume_toolkit = Toolkit(name="resume-tools", tools=[WebSearchTool(), SaveCandidateDetails()])

# Resume agent needs to take in a file, process the file, save the file and results to the room
# Agent should compare the resume to other job descriptions and indicate if the person is a match for them
# @service.path(identity="resume-runner", path="/resumerunner")
# class ResumeRunner(LLMTaskRunner):
#     def __init__(self):
#         super().__init__(
#             name="resume-runner",
#             title="resume-runner",
#             description="A TaskRunner that processes Resumes",
#             llm_adapter=OpenAIResponsesAdapter(),
#             supports_tools=True,
#             toolkits=[resume_toolkit, StorageToolkit()],
#             # input_schema={"prompt":""},
#             rules=[
#                 "You process resumes to determine if candidates are a good fit for open roles",
#                 "When invoked, you MUST first call the get-resume tool with the provided resume_path to obtain the resume file.",
#                 "Next extract the person's name, contact information, skills, and a concise experience summary",
#                 "Once you have extracted skills from their resume, look them up on LinkedIn and Google to see if you can find additional information about the candidate",
#                 "Once you have collected enough information about the candidate, save their information to the candidate database using the save-candidate-details tool"
#             ]
#         )
#     async def start(self, *, room):
#         await super().start(room=room)
#         log.info("creating tables if they do not exist")
#         await room.database.create_table_with_schema(
#             name="candidates",
#             schema={
#                 "resume_path": TextDataType(),
#                 "candidate_name": TextDataType(),
#                 "contact_info": TextDataType(),
#                 "resume_text": TextDataType(),
#                 "resume_summary": TextDataType(), 
#                 "web_search_notes": TextDataType()
#             },
#             mode="create_if_not_exists"
#         )
#         log.info("finished creating tables")

#     # Override ask to avoid duplicating toolkits (context.toolkits already contains self._toolkits)
#     async def ask(self, *, context: AgentCallContext, arguments: dict):
#         prompt = arguments.get("prompt")
#         if prompt is None:
#             raise ValueError("`prompt` is required")

#         context.chat.append_user_message(prompt)

#         resp = await self._llm_adapter.next(
#             context=context.chat,
#             room=context.room,
#             toolkits=context.toolkits,  # already includes this agent's toolkits need to fix potential bug in LLMRunner
#             tool_adapter=self._tool_adapter,
#             output_schema=self.output_schema,
#         )

#         if self.output_schema is None:
#             return TextResponse(text=resp)
#         return resp
    
# @service.path(identity="resume-mailbot", path="/resume-mailbot")  
# class ResumeMailbot(MailWorker):
#     def __init__(self):
#         super().__init__(
#             name="resume-mailbot",
#             title="resume-mailbot",
#             description="A mail agent that processes resumes",
#             llm_adapter=OpenAIResponsesAdapter,
#             toolkits=[Toolkit(name="web-search", tools=[WebSearchTool()]), StorageToolkit(), SaveCandidateDetails()],
#             queue="resume_email", # update later
#             email_address="jobs@mail.meshagent.life" # update later
#         )

asyncio.run(service.run())