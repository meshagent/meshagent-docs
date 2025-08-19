from meshagent.api import RequiredToolkit
from meshagent.agents.chat import ChatBot
from meshagent.openai import OpenAIResponsesAdapter
import asyncio

from meshagent.api.services import ServiceHost

service = ServiceHost()


@service.path("/agent")
class CoderChatbot(ChatBot):
    def __init__(self):
        super().__init__(
            name="meshagent.chatbot.coder",
            title="coder",
            description="a chatbot that knows how to code",
            rules=[
                "you are a code assistant that can write code for users and help them with programming questions",
                "if asked to write code, prefer to write it to files directly and then display the files to the user instead of returning it in the chat",
                "unless asked by the user about the code inside a file, do not include code in your responses",
                "after writing code to a file, you MUST use the display_document tool to show it to the user",
            ],
            llm_adapter=OpenAIResponsesAdapter(model="o3-mini"),
            labels=["chatbot", "code"],
            requires=[
                RequiredToolkit(
                    name="ui",
                    tools=[
                        "display_document",
                    ],
                ),
                RequiredToolkit(name="storage"),
                RequiredToolkit(
                    name="meshagent.markitdown",
                    tools=["markitdown_from_file"],
                ),
            ],
        )


asyncio.run(service.run())
