from meshagent.api import RequiredToolkit
from meshagent.agents.chat import ChatBot
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.api.services import ServiceHost
from meshagent.markitdown.tools import MarkItDownToolkit

import asyncio

service = ServiceHost()


@service.path("/agent")
class SimpleChatbot(ChatBot):
    def __init__(self):
        super().__init__(
            name="meshagent.chatbot",
            title="chatbot",
            description="an simple chatbot",
            rules=[],
            llm_adapter=OpenAIResponsesAdapter(),
            toolkits=[
                MarkItDownToolkit()
            ],
        )


asyncio.run(service.run())
