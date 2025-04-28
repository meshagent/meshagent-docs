import asyncio

from meshagent.api import RoomClient, websocket_protocol

async def main():
    room_name = "examples"

    async with RoomClient(protocol=websocket_protocol(
        participant_name="sample_user",
        room_name=room_name
    )) as room:
        
        result = await room.agents.invoke_tool(toolkit="samples.adder-tool", tool="adder", arguments={"a":1, "b":2})
        print(f"The result was {result}")       

asyncio.run(main())
    