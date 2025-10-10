import os
import uuid
import asyncio
from datetime import datetime, date
from openai import AsyncOpenAI
from livekit.agents import function_tool, ChatContext, Agent, RunContext, AgentSession
from livekit.plugins import openai, silero

from meshagent.api import RequiredToolkit, RequiredSchema
from meshagent.livekit.agents.voice import VoiceBot
from meshagent.api.services import ServiceHost
from meshagent.tools.document_tools import (
    DocumentAuthoringToolkit,
    DocumentTypeAuthoringToolkit,
)
from meshagent.agents.schemas.document import document_schema
from meshagent.api.room_server_client import TextDataType, TimestampDataType
from meshagent.api.messaging import TextResponse, JsonResponse
from meshagent.tools import Tool, Toolkit, ToolContext
from meshagent.otel import otel_config

service = ServiceHost()

otel_config(
    service_name="my-service"
)  # automatically enables telemetry data collection for your agents and tools


class WriteTask(Tool):
    def __init__(self):
        super().__init__(
            name="WriteTask",
            title="Add a task",
            description="A tool to add tasks to the database",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["taskdescription"],
                "properties": {"taskdescription": {"type": "string"}},
            },
        )

    async def execute(self, context, taskdescription: str):
        await context.room.database.insert(
            table="tasks",
            records=[
                {"task_id": str(uuid.uuid4()), "taskdescription": taskdescription}
            ],
        )
        return TextResponse(text="Task added!")


class GetTasks(Tool):
    def __init__(self):
        super().__init__(
            name="GetTasks",
            title="List tasks",
            description="List tasks recorded today or this week",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": [],
                "properties": {},
            },
        )

    async def execute(self, context):
        return JsonResponse(
            json={"values": await context.room.database.search(table="tasks")}
        )


@service.path("/voice")
class SimpleVoicebot(VoiceBot):
    def __init__(self):
        super().__init__(
            name="voice_agent",
            title="voice_agent",
            description="a sample voicebot",
            rules=[
                "Always respond to the user and include a fun fact at the end of your response.",
                "keep your answers short and sweet and be friendly DO NOT include emojis in your response",
                "Use the ask_user tool to pick the name of a document, pick a document name if the tool is not available.",
                "The document names MUST have the extension .document, automatically add the extension if it is not provided",
                "You MUST always write content to a document",
                "First open a document, then use tools to write the document content before closing the document",
                "Before closing the document, ask the user if they would like any additional modifications to be made to the document, and if so, make them. continue to ask the user until they are happy with the contents. you are not finished until the user is happy.",
                "Blob URLs MUST not be added to documents, they must be saved as files first",
            ],
            requires=[
                RequiredToolkit(name="ui"),
                RequiredSchema(name="document"),
                RequiredToolkit(
                    name="meshagent.markitdown", tools=["markitdown_from_file"]
                ),
            ],
            toolkits=[
                DocumentAuthoringToolkit(),
                DocumentTypeAuthoringToolkit(
                    schema=document_schema, document_type="document"
                ),
                Toolkit(name="tasktools", tools=[WriteTask(), GetTasks()]),
            ],
        )

    async def start(self, *, room):
        await super().start(room=room)
        # One tiny table:
        await room.database.create_table_with_schema(
            name="tasks",
            schema={"task_id": TextDataType(), "taskdescription": TextDataType()},
            mode="overwrite",
            data=None,
        )

    def create_session(self, *, context: ToolContext) -> AgentSession:
        token: str = context.room.protocol.token
        url: str = context.room.room_url

        room_proxy_url = f"{url}/v1"

        oaiclient = AsyncOpenAI(
            api_key=token,
            base_url=room_proxy_url,
            default_headers={"Meshagent-Session": context.room.session_id},
        )

        session = AgentSession(
            max_tool_steps=50,
            allow_interruptions=True,
            vad=silero.VAD.load(),
            stt=openai.STT(client=oaiclient),
            tts=openai.TTS(client=oaiclient, voice="sage"),
            llm=openai.LLM(client=oaiclient, model="gpt-4.1"),
        )
        return session

    async def create_agent(self, *, context, session):
        ctx = ChatContext()
        today_str = date.today().strftime("%A %B %-d")
        ctx.add_message(role="assistant", content=f"Today's date is: {today_str}")

        @function_tool
        async def say(context: RunContext, text: str):
            "says something out loud to the user"
            session.say(text)
            return "success"

        return Agent(
            chat_ctx=ctx,
            instructions="\n".join(self.rules),
            allow_interruptions=True,
            tools=[*await self.make_function_tools(context=context), say],
        )


asyncio.run(service.run())
