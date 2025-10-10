# main.py
import asyncio
from meshagent.api.services import ServiceHost
from meshagent.agents.chat import ChatBot
from meshagent.openai import OpenAIResponsesAdapter

host = ServiceHost()


@host.path("/agent")
class MyChatBot(ChatBot):
    def __init__(self):
        super().__init__(
            name="chatbot",  # participant name for the agent in the room
            rules=[],  # optional rules for the agent
            llm_adapter=OpenAIResponsesAdapter(),
        )


print(f"Running on port {host.port}")
asyncio.run(host.run())
