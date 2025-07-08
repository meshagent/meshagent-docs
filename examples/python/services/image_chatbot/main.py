from meshagent.tools import Toolkit
from meshagent.tools.storage import SaveFileFromUrlTool
from meshagent.agents.chat import ChatBot, ChatBotThreadOpenAIImageGenerationTool
from meshagent.openai import OpenAIResponsesAdapter


import asyncio

from meshagent.api.services import ServiceHost

service = ServiceHost()

@service.path("/agent")
class ImageChatbot(ChatBot):
    def __init__(self):
        super().__init__(
            name="meshagent.image-chatbot",
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
                    ChatBotThreadOpenAIImageGenerationTool(thread_context=thread_context)
                ]
            )
        ]
    

asyncio.run(service.run())
