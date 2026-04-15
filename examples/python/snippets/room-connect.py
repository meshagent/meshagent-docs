import asyncio
from meshagent.api import RoomClient


async def main():
    # Run with:
    # meshagent room connect --room=my-room --identity=participant -- python3 room-connect.py
    async with RoomClient() as room:
        print(f"Connected to room: {room.room_name}")


asyncio.run(main())
