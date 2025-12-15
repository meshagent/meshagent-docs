import asyncio
import logging
import os
from meshagent.api import RequiredToolkit
from meshagent.tools import Tool, Toolkit, ToolContext, RemoteToolkit
from meshagent.api.messaging import FileResponse, JsonResponse, TextResponse
from meshagent.openai.tools.responses_adapter import WebSearchTool
from meshagent.agents.llmrunner import LLMTaskRunner
from meshagent.otel import otel_config
from meshagent.agents.agent import AgentCallContext
from meshagent.tools.storage import StorageToolkit
from meshagent.agents.mail import MailWorker

log = logging.getLogger("resume-runner")

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
        DEFAULT_RESUME_PROMPT = f"Process the candidate resume located at: {target_path}. You must extract the candidate's name and contact information from their resume and generate a succinct summary of their skills and experience. You must also use the web search tool to look for additional information about the candidate. Beware that some candidates may have common names and so it may be more difficult for you to find information about them. Once you have collected sufficient information about the candidate, store their information in the candidates table in the database."

        resume_processing_prompt = os.getenv("") or DEFAULT_RESUME_PROMPT
        log.info(f"Processing resume with prompt: {resume_processing_prompt}")

        response = await context.room.agents.ask(
            agent="meshagent.runner",
            arguments={"prompt":resume_processing_prompt, 
                       "model":"gpt-5.2", 
                       "tools":[
                           {"name":"storage"}, # remove this later maybe just give bytes? 
                           {"name":"web_search"},
                        #    {
                        #        "name": "database",
                        #        "tables": ["candidates"],
                        #        "read_only": False,
                        #    },
                        ]
                    },
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

# @service.path(identity="mailbot-toolkit", path="/mailbot-toolkit")
class MailBotToolkit(RemoteToolkit):
    def __init__(self):
        super().__init__(
            name="mailbot-toolkit",
            title="mailbot-toolkit",
            description="A Toolkit for the MailWorker to kickoff resume processing",
            tools=[
                ProcessResume()
            ],
        )    

# asyncio.run(service.run())
