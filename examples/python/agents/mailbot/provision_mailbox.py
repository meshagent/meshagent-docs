import os
import asyncio
import aiohttp
import logging
from meshagent.api import Meshagent

log = logging.getLogger()


async def provision_mailbox() -> None:
    meshagent = Meshagent()
    try:
        await meshagent.create_mailbox(
            project_id=os.environ["MESHAGENT_PROJECT_ID"],
            address=os.environ["EMAIL_ADDRESS"],
            room=os.environ["ROOM_NAME"],
            queue=os.environ["EMAIL_QUEUE"],
        )
        log.info(
            "Created mailbox %s for room %s",
            os.environ["EMAIL_ADDRESS"],
            os.environ["ROOM_NAME"],
        )
    except aiohttp.ClientResponseError as exc:
        if exc.status == 409:
            raise RuntimeError(
                f"Mailbox '{os.environ['EMAIL_ADDRESS']}' already exists. Choose a different EMAIL_ADDRESS and try again."
            ) from exc
        raise
    finally:
        await meshagent.close()


asyncio.run(provision_mailbox())
