from meshagent.api import RequiredToolkit, RequiredSchema
from meshagent.tools import Toolkit
from meshagent.agents.schemas.gallery import gallery_schema
from meshagent.tools.storage import SaveFileFromUrlTool
from meshagent.tools.document_tools import DocumentAuthoringToolkit, DocumentTypeAuthoringToolkit
from meshagent.agents.chat import ChatBot
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.openai.tools.responses_adapter import WebSearchTool

from meshagent.agents.thread_schema import thread_schema

import asyncio
import os

from meshagent.api import SchemaRegistry, SchemaRegistration

from meshagent.api.services import ServiceHost

service = ServiceHost()

@service.path("/thread")
class ThreadSchema(SchemaRegistry):
    def __init__(self):
        super().__init__(
            name="thread",
            schemas=[
                SchemaRegistration(
                    name="thread",
                    schema=thread_schema
                )
            ]
        )

@service.path("/agent")
class WebSearchChatbot(ChatBot):
    def __init__(self):
        super().__init__(
            name="meshagent.web-search-chatbot",
            title="image designer",
            description="an agent that generates images and videos",
            empty_state_title="What images can I make for you?",
            rules=[
                "you are an assistant for generating images"
            ],
            llm_adapter = OpenAIResponsesAdapter(parallel_tool_calls=True),
            requires = [
            ],
            toolkits=[
                
                Toolkit(name="local", tools=[
                    SaveFileFromUrlTool()
                ]),
            ],
            auto_greet_message="What images can I help you design?",
            labels=[ "tasks", "images" ]
        )

    async def get_thread_toolkits(self, *, thread_context, participant):
        return [
            Toolkit(
                name="builtin",
                tools=[
                    WebSearchTool()
                ]
            )
        ]
    

asyncio.run(service.run())
