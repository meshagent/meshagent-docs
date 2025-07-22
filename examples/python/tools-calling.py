import asyncio

from meshagent.api import RoomClient, websocket_protocol

async def main():
    room_name = "toolsroom"

    async with RoomClient(
        protocol=websocket_protocol(participant_name="sample_user", room_name=room_name)
    ) as room:
        add_result = await room.agents.invoke_tool(
            toolkit="math-toolkit", tool="add", arguments={"a": 1, "b": 2}
        )
        print(f"The result from adding the numbers is: {add_result}")

        subtract_result = await room.agents.invoke_tool(
            toolkit="math-toolkit", tool="subtract", arguments={"a": 1, "b": 2}
        )
        print(f"The result from subtracting the numbers is: {subtract_result}")


asyncio.run(main())
