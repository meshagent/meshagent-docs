import asyncio
from meshagent.api import RoomClient, websocket_protocol


async def main():
    # Define a unique room name
    room_name = "my-room"
    participant_name = "my-participant"

    async with RoomClient(
        protocol=websocket_protocol(
            participant_name=participant_name, room_name=room_name
        )
    ) as room:
        print("connected to room")


asyncio.run(main())
