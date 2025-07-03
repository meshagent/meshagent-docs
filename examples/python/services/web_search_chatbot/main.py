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


@service.path("/agent")
class WebSearchChatbot(ChatBot):
    def __init__(self):
        super().__init__(
            name="meshagent.web-search-chatbot",
            title="web search",
            description="an agent can search the web",
            empty_state_title="What can I do for you",
            rules=[
                "you are an assistant for searching the web"
            ],
            llm_adapter = OpenAIResponsesAdapter(parallel_tool_calls=True),
            requires = [
            ],
            toolkits=[
                
                Toolkit(name="local", tools=[
                    SaveFileFromUrlTool()
                ]),
            ],
            auto_greet_message="What can I do for you?",
            labels=[ "tasks", "websearch" ]
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
