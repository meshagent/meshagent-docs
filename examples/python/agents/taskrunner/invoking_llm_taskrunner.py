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

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# make sure you have set your env variables for MeshAgent
api_key = os.getenv("MESHAGENT_API_KEY")
if not api_key:
    raise RuntimeError("Set MESHAGENT_API_KEY before running this script.")


async def run_dynamic_llm_taskrunner(
    room_name: str, agent_name: str, prompt: str, output_schema: dict
):
    """
    Run the Dynamic LLM TaskRunner in a MeshAgent Room

    Args:
        room_name: Name of the room to connect to
        agent_name: Name of the agent to run
        prompt: The user prompt to send to the agent
        output_schema: The structured output schema to use in the response
        participant_name: Name to use as participant (defaults to "test_user")
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
                agent=agent_name,
                arguments={"prompt": prompt, "output_schema": output_schema},
            )
            log.info(f"Response: {response}")
            return response
    except Exception as e:
        log.error(f"Connection failed:{e}")
        raise

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
    run_dynamic_llm_taskrunner(
        room_name="myroom",
        agent_name="dynamicllmtaskrunner",
        prompt="Create a product listing for a bluetooth speaker",
        output_schema=product_schema,
    )
)
