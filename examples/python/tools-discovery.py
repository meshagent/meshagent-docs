import asyncio

from meshagent.api import RoomClient, websocket_protocol


async def main():
    room_name = "toolsroom"

    async with RoomClient(
        protocol=websocket_protocol(participant_name="sample_user", room_name=room_name)
    ) as room:
        toolkits = await room.agents.list_toolkits()

        print("The tools connected to our room are:")
        for toolkit in toolkits:
            print(f"\n Toolkit: {toolkit.name}: {toolkit.title} - {toolkit.description}")
            for tool in toolkit.tools:
                print(f" Tool: {tool.name}: {tool.title} - {tool.description}")

        agents = await room.agents.list_agents()
        print("The agents in the room are:")
        for agent in agents:
            print(f"Agent: {agent.name}")


asyncio.run(main())