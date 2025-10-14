import os
import asyncio
import logging
from meshagent.api import (
    RoomClient,
    WebSocketClientProtocol,
    ParticipantToken,
    ApiScope,
    ParticipantGrant,
)
from meshagent.api.helpers import websocket_room_url
from meshagent.otel import otel_config

otel_config(service_name="taskrunner")
log = logging.getLogger("taskrunner")

api_key = os.getenv("MESHAGENT_API_KEY")
if not api_key:
    raise RuntimeError("Set MESHAGENT_API_KEY before running this script.")


async def run_schema_planner(room_name: str, prompt: str, output_schema: dict):
    """
    Connect to a MeshAgent room and ask the built-in Schema Planner to produce
    a structured response that conforms to `output_schema`.

    Args:
        room_name: Name of the room to connect to
        prompt: The task description / instruction
        output_schema: The structured JSON output schema the agent must respond with
    """
    token = ParticipantToken(
        name="sample-participant",
        grants=[
            ParticipantGrant(name="room", scope=room_name),
            ParticipantGrant(name="role", scope="agent"),
            ParticipantGrant(name="api", scope=ApiScope.agent_default()),
        ],
    ).to_jwt(api_key=api_key)

    protocol = WebSocketClientProtocol(
        url=websocket_room_url(room_name=room_name), token=token
    )
    try:
        async with RoomClient(protocol=protocol) as room:
            log.info(f"Connected to room: {room.room_name}")
            response = await room.agents.ask(
                agent="meshagent.schema_planner",
                arguments={"prompt": prompt, "output_schema": output_schema},
            )
            log.info(f"Response: {response}")
            return response
    except Exception as e:
        print(f"Connection failed: {e}")


# Try it with a sample schema
product_schema = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "title": {"type": "string"},
        "price": {"type": "number"},
        "features": {"type": "array", "items": {"type": "string"}},
        "description": {"type": "string"},
    },
    "required": ["title", "price", "features", "description"],
}

asyncio.run(
    run_schema_planner(
        room_name="test",
        prompt="Create a product listing for a bluetooth speaker",
        output_schema=product_schema,
    )
)
