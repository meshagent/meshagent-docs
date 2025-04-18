import asyncio
from meshagent.api import RoomClient, websocket_protocol

async def main():    
    # Define a unique room name
    room_name = 'my-room'
    participant_name = 'my-participant'

    async with RoomClient(
        protocol=websocket_protocol(
            participant_name=participant_name,
            room_name=room_name
        )) as room:   
            print("connected to room")

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(main())

