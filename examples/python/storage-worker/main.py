from meshagent.agents.worker import Worker
from meshagent.openai.tools import OpenAIResponsesAdapter, OpenAIResponsesToolResponseAdapter
from meshagent.api import RequiredToolkit
from meshagent.api.services import ServiceHost
from meshagent.tools.storage import StorageToolkit
import asyncio
import os
import logging


logging.basicConfig(level=logging.INFO)

host = ServiceHost(
    port=7001
)


logger = logging.getLogger("worker")
logger.info(f"Listening on {os.getenv("WORKER_QUEUE")}")

@host.path("/worker")
class StorageWorker(Worker):

    def __init__(self):
        super().__init__(
            queue=os.getenv("WORKER_QUEUE"),
            name="storage-worker",
            title="storage worker sample",
            description="this sample reads messages from a queue",
            toolkits=[
                StorageToolkit()
            ],
            llm_adapter=OpenAIResponsesAdapter(),
            tool_adapter=OpenAIResponsesToolResponseAdapter(),
            rules=[
                "you will receive a message with instructions, process it and do what it says",
                "you are not an interactive agent so you must not ask the user questions",
            ])
        
    async def process_message(self, *, chat_context, room, message, toolkits):
        logger.info(f"processing {message}")
        response = await super().process_message(chat_context=chat_context, room=room, message=message, toolkits=toolkits)
        logger.info(f"response {response}")


asyncio.run(host.run())
