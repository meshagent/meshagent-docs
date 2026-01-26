import os
import asyncio
import json
import logging
from typing import Dict, Any
from meshagent.api import (
    RoomClient,
    WebSocketClientProtocol,
    ParticipantToken,
    ApiScope,
    ParticipantGrant,
)
from meshagent.api.helpers import websocket_room_url
from meshagent.otel import otel_config

otel_config()
log = logging.getLogger(__name__)

api_key = os.getenv("MESHAGENT_API_KEY")
if not api_key:
    raise RuntimeError("Set MESHAGENT_API_KEY before running this script.")


async def call_agent(
    room_name: str, agent_name: str, arguments: Dict[str, Any]
) -> Dict[str, Any]:
    """Invoke a TaskRunner tool with the given arguments."""
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
            tool_name = f"run_{agent_name}_task"
            result = await room.agents.invoke_tool(
                toolkit=agent_name,
                tool=tool_name,
                arguments=arguments,
            )
            # Extract JSON data from JsonBody response
            return result.json if hasattr(result, "json") else result
    except Exception as e:
        log.error(f"Connection failed:{e}")
        raise


async def main():
    # Call your translator
    result = await call_agent(
        room_name="translate",
        agent_name="translator",
        arguments={"text": "Hello, how are you today?"},
    )

    print("Translation result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
