import asyncio
from meshagent.api import RoomClient


async def main():
    # Run with:
    # meshagent room connect --room=my-room --identity=participant-name -- python3 documents-writing.py
    path = "hello-world.document"

    async with RoomClient() as room:
        print(f"Connected to room: {room.room_name}")
        document = await room.sync.open(path=path, create=True)
        try:
            await document.synchronized
            document.root.append_child(
                tag_name="body", attributes={"text": "hello world!"}
            )
            await asyncio.sleep(1)
        finally:
            await room.sync.close(path=path)


asyncio.run(main())
