import os
import asyncio
from meshagent.api import (
    RoomClient,
    WebSocketClientProtocol,
    ParticipantToken,
    ApiScope,
    ParticipantGrant,
)


def env(name: str) -> str:
    val = os.getenv(name)
    if not isinstance(val, str) or not val:
        raise RuntimeError(f"Missing required environment variable: {name}.")
    return val


async def main():
    room_name = "my-room"
    api_key = env("MESHAGENT_API_KEY")
    async with RoomClient(
        protocol=WebSocketClientProtocol(
            url=f"wss://api.meshagent.com/rooms/{room_name}",
            token=ParticipantToken(
                name="participant",
                grants=[
                    ParticipantGrant(name="room", scope=room_name),
                    ParticipantGrant(name="role", scope="agent"),
                    ParticipantGrant(name="api", scope=ApiScope.agent_default()),
                ],
            ).to_jwt(api_key=api_key),
        )
    ) as room:
        print(f"Connected to room: {room.room_name}")


asyncio.run(main())
