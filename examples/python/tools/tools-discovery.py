import os
import asyncio
import logging
from meshagent.api import RoomClient, WebSocketClientProtocol, ParticipantToken, ApiScope, ParticipantGrant
from meshagent.api.helpers import meshagent_base_url, websocket_room_url

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def env(name: str) -> str:
    val = os.getenv(name)
    if not isinstance(val, str) or not val:
        raise RuntimeError(f"Missing required environment variable: {name}. Try running meshagent env in the terminal to export the required environment variables.")
    return val

async def main():
    room_name = "toolsroom"

    async with RoomClient(
        protocol=WebSocketClientProtocol(
                url=websocket_room_url(room_name=room_name, base_url=meshagent_base_url()),
                token=ParticipantToken(
                    name="participant",
                    project_id=env("MESHAGENT_PROJECT_ID"),
                    api_key_id=env("MESHAGENT_KEY_ID"),
                    grants=[
                        ParticipantGrant(name="room", scope=room_name),
                        ParticipantGrant(name="role", scope="agent"),
                        ParticipantGrant(name="api", scope=ApiScope.agent_default()),
                    ],
                ).to_jwt(token=env("MESHAGENT_SECRET")),
            )
    ) as room:
        log.info(f"Connected to room: {room.room_name}")
        toolkits = await room.agents.list_toolkits()

        print("The tools connected to our room are:")
        for toolkit in toolkits:
            print(
                f"\n Toolkit: {toolkit.name}: {toolkit.title} - {toolkit.description}"
            )
            for tool in toolkit.tools:
                print(f" Tool: {tool.name}: {tool.title} - {tool.description}")

        agents = await room.agents.list_agents()
        print("The agents in the room are:")
        for agent in agents:
            print(f"Agent: {agent.name}")


asyncio.run(main())
