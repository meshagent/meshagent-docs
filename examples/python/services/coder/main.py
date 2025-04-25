from meshagent.api import RequiredToolkit
from meshagent.agents.hosting import RemoteAgentServer
from meshagent.agents.chat import ChatBot
from meshagent.openai import OpenAIResponsesAdapter
import asyncio
import os

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
                "after writing code to a file, you MUST use the display_document tool to show it to the user"
            ],
            llm_adapter = OpenAIResponsesAdapter(
                model="o3-mini"
            ),
            labels=[ "chatbot", "code" ],
            requires=[
                RequiredToolkit(name="ui",
                    tools=[
                        "display_document",
                    ]
                ),
                RequiredToolkit(
                    name="storage"
                ),
                RequiredToolkit(
                    name="meshagent.markitdown",
                    tools=[ "markitdown_from_user", "markitdown_from_file" ]
                ),
            ]
        )
        

async def server():

    remote_agent_server = RemoteAgentServer(
        cls=CoderChatbot,
        path="/webhook",
        validate_webhook_secret=False,
        port=int(os.getenv("MESHAGENT_PORT"))
    )
    await remote_agent_server.run()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(server())