import os
import asyncio
import logging
from typing import Optional, Dict, Any
from meshagent.api import (
    ApiScope,
    ParticipantGrant,
    ParticipantToken,
    RoomClient,
    WebSocketClientProtocol,
)
from meshagent.api.helpers import websocket_room_url
from meshagent.otel import otel_config

otel_config(service_name="llm-taskrunner-demo")
log = logging.getLogger("llm-taskrunner-demo")

# ---- Simple configuration knobs (edit these) ----
ROOM_NAME = "myroom"
PROMPT_TEXT = "Create a product listing for a bluetooth speaker"
RUN_LLMTASKRUNNER = True
RUN_DYNAMIC = True
# -------------------------------------------------

API_KEY = os.getenv("MESHAGENT_API_KEY")
if not API_KEY:
    raise RuntimeError("Set MESHAGENT_API_KEY before running this script.")


def default_product_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["title", "price", "features", "description"],
        "properties": {
            "title": {"type": "string"},
            "price": {"type": "number"},
            "features": {"type": "array", "items": {"type": "string"}},
            "description": {"type": "string"},
        },
    }


async def ask_agent(*, room_name: str, agent_name: str, arguments: Dict[str, Any]):
    token = ParticipantToken(
        name="sample-participant",
        grants=[
            ParticipantGrant(name="room", scope=room_name),
            ParticipantGrant(name="role", scope="agent"),
            ParticipantGrant(name="api", scope=ApiScope.agent_default()),
        ],
    ).to_jwt(api_key=API_KEY)

    protocol = WebSocketClientProtocol(
        url=websocket_room_url(room_name=room_name), token=token
    )

    async with RoomClient(protocol=protocol) as room:
        log.info("Connected to room: %s", room.room_name)
        resp = await room.agents.ask(agent=agent_name, arguments=arguments)
        log.info("Response from %s: %s", agent_name, resp)
        return resp


async def main():
    # 1) Fixed-schema runner
    if RUN_LLMTASKRUNNER:
        await ask_agent(
            room_name=ROOM_NAME,
            agent_name="llmtaskrunner",
            arguments={"prompt": PROMPT_TEXT},
        )

    # 2) Dynamic-schema runner
    if RUN_DYNAMIC:
        schema = default_product_schema()
        await ask_agent(
            room_name=ROOM_NAME,
            agent_name="dynamicllmtaskrunner",
            arguments={"prompt": PROMPT_TEXT, "output_schema": schema},
        )


if __name__ == "__main__":
    asyncio.run(main())
