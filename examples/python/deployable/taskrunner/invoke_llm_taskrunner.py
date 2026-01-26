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


async def invoke_taskrunner(room_name: str, prompt: str):
    """
    Connect to a MeshAgent room and invoke a joined LLMTaskRunner tool.

    Args:
        room_name: Target room
        prompt: The text to send to the task runner
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
            response = await room.agents.invoke_tool(
                toolkit="llmtaskrunner",
                tool="run_llmtaskrunner_task",
                arguments={"prompt": prompt, "tools": [], "model": None},
            )
            log.info(f"Response: {response}")
            return response
    except Exception as e:
        log.error(f"Connection failed:{e}")
        raise


asyncio.run(
    invoke_taskrunner(
        room_name="quickstart",
        prompt="Write a poem about AI agents",
    )
)
