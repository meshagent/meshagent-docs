import asyncio,json
from pathlib import Path
from meshagent.api.client import Meshagent

# async def main():
#     async with Meshagent() as client:  # uses env vars by default
#         projects = await client.list_projects()
#         print(projects)

# asyncio.run(main())

import os
import asyncio
from meshagent.api import (
    RoomClient,
    WebSocketClientProtocol,
    ParticipantToken,
    ApiScope,
    ParticipantGrant,
)

def env(name: str) -> str:
    val = os.getenv(name)
    if not isinstance(val, str) or not val:
        raise RuntimeError(f"Missing required environment variable: {name}.")
    return val


# async def main():
#     room_name = "tula"
#     api_key = env("MESHAGENT_API_KEY")
#     async with RoomClient(
#         protocol=WebSocketClientProtocol(
#             url=f"wss://api.meshagent.life/rooms/{room_name}", # CHANGE TO LIFE OR COM DEPENDING ON WHERE RUNNING!
#             token=ParticipantToken(
#                 name="participant",
#                 grants=[
#                     ParticipantGrant(name="room", scope=room_name),
#                     ParticipantGrant(name="role", scope="agent"),
#                     ParticipantGrant(name="api", scope=ApiScope.agent_default()),
#                 ],
#             ).to_jwt(api_key=api_key),
#         )
#     ) as room:
#         print(f"Connected to room: {room.room_name}")

# asyncio.run(main())

# SESSION = Path("~/.meshagent/session.json").expanduser()
# tokens = json.loads(SESSION.read_text())
# access_token = tokens["access_token"]

# async def main():
#     client = Meshagent(base_url="https://api.meshagent.life", token=access_token) 
#     # try:
#     #     role = await client.get_project_role("1fd090a4-8dc5-4918-948b-2b1b2c981eb0")
#     #     print("Valid key, role:", role)
#     # except Exception as e:
#     #     print("Key failed:", e)
#     try:
#         projects = await client.list_projects()
#         print(projects)
#     finally:
#         await client.close()

# asyncio.run(main())


import asyncio
from meshagent.api.client import Meshagent
from meshagent.cli.auth_async import get_access_token

async def main():
    access_token = await get_access_token()
    client = Meshagent(token=access_token)
    try:
        projects = await client.list_projects()
        client.
        print(projects)
    finally:
        await client.close()

asyncio.run(main())
