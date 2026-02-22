import asyncio
import uuid

from meshagent.agents.chat import ChatBot
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.openai.tools.responses_adapter import WebSearchToolkitBuilder
from meshagent.api.services import ServiceHost
from meshagent.tools.storage import StorageToolkit
from meshagent.tools.document_tools import (
    DocumentAuthoringToolkit,
    DocumentTypeAuthoringToolkit,
)
from meshagent.agents.schemas.document import document_schema
from meshagent.api.room_server_client import TextDataType
from meshagent.api.messaging import TextContent, JsonContent
from meshagent.tools import Tool, Toolkit
from meshagent.otel import otel_config

service = ServiceHost()  # port defaults to an available port if not assigned

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
        return TextContent(text="Task added!")


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
        return JsonContent(
            json={"values": await context.room.database.search(table="tasks")}
        )


@service.path(path="/chat", identity="mychatbot")
class SimpleChatbot(ChatBot):
    def __init__(self):
        super().__init__(
            name="mychatbot",
            title="mychatbot",
            description="a simple chatbot",
            rules=[
                "Always respond to the user and include a fun fact at the end of your response.",
                "use the ask_user tool to pick the name of a document, pick a document name if the tool is not available.",
                "the document names MUST have the extension .document, automatically add the extension if it is not provided",
                "you MUST always write content to a document",
                "first open a document, then use tools to write the document content before closing the document",
                "before closing the document, ask the user if they would like any additional modifications to be made to the document, and if so, make them. continue to ask the user until they are happy with the contents. you are not finished until the user is happy.",
                "blob URLs MUST not be added to documents, they must be saved as files first",
            ],
            llm_adapter=OpenAIResponsesAdapter(),
            toolkits=[  # Add built in and custom tools here!
                StorageToolkit(),
                DocumentAuthoringToolkit(),
                DocumentTypeAuthoringToolkit(
                    schema=document_schema, document_type="document"
                ),
                Toolkit(name="tasktracker", tools=[WriteTask(), GetTasks()]),
            ],
        )

    def get_toolkit_builders(self):
        builders = super().get_toolkit_builders()
        builders.append(WebSearchToolkitBuilder())  # add web search
        return builders

    async def start(self, *, room):
        await super().start(room=room)
        # One tiny table:
        await room.database.create_table_with_schema(
            name="tasks",
            schema={"task_id": TextDataType(), "taskdescription": TextDataType()},
            mode="create_if_not_exists",
            data=None,
        )


asyncio.run(service.run())
