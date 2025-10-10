import os
import asyncio
import aiohttp
import logging
from meshagent.otel import otel_config
from meshagent.api import Meshagent
from meshagent.api.services import ServiceHost
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.agents.mail import MailWorker

# Enable OpenTelemetry logging and tracing for the agent
otel_config(service_name="mailbot")
log = logging.getLogger("mailbot")

queue = os.environ["EMAIL_QUEUE"]
email_address = os.environ["EMAIL_ADDRESS"]
project_id = os.environ["MESHAGENT_PROJECT_ID"]

service = ServiceHost()  # MeshAgent assigns a free port if you omit one


async def ensure_mailbox(*, room_name: str) -> None:
    meshagent = Meshagent(base_url=os.getenv("MESHAGENT_BASE_URL"))
    try:
        await meshagent.create_mailbox(
            project_id=project_id,
            address=email_address,
            room=room_name,
            queue=queue,
        )
        log.info("Created mailbox %s for room %s", email_address, room_name)
    except aiohttp.ClientResponseError as exc:
        if exc.status == 409:
            raise RuntimeError(
                f"Mailbox '{email_address}' already exists. Choose a different EMAIL_ADDRESS and try again."
            ) from exc
        raise
    finally:
        await meshagent.close()


@service.path(path="/mail", identity="mailbot")
class ExampleMailbot(MailWorker):
    def __init__(self):
        super().__init__(
            name="mailbot",
            title="mailbot",
            description="An agent that responds via email",
            llm_adapter=OpenAIResponsesAdapter(),
            rules=["You are a helpful assistant that responds to users via email."],
            queue=queue,
            email_address=email_address,
        )
        self._mailbox_ready = False

    async def start(self, *, room):
        if not self._mailbox_ready:
            await ensure_mailbox(room_name=room.room_name)
            self._mailbox_ready = True
        await super().start(room=room)


asyncio.run(service.run())
