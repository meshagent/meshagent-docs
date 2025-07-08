import asyncio

from meshagent.api import RoomClient, websocket_protocol


async def main():
    room_name = "examples"

    async with RoomClient(
        protocol=websocket_protocol(participant_name="sample_user", room_name=room_name)
    ) as room:
        toolkits = await room.agents.list_toolkits()

        print("The tools connected to our room are:")
        for toolkit in toolkits:
            print(f"\n{toolkit.name}: {toolkit.title} - {toolkit.description}")
            for tool in toolkit.tools:
                print(f"  {tool.name}: {tool.title} - {tool.description}")


asyncio.run(main())
