import asyncio
from meshagent.api import RoomClient, WebSocketClientProtocol, websocket_room_url
import os

async def push():
    async with RoomClient(
        protocol=WebSocketClientProtocol(
            url=websocket_room_url(room_name=os.getenv("ROOM")), 
            token=os.getenv("TOKEN")
            )
    ) as room:
        await room.queues.send(
            name=os.getenv("WORKER_QUEUE"), 
            message={ "instructions" : "save a poem about ai to poem.txt"}
            ) 

asyncio.run(push())