import asyncio
import os
from meshagent.api import RoomClient


async def main():
    # Run with:
    # meshagent room connect --room=quickstart --identity=my-user -- python3 quickstart-agent.py
    async with RoomClient() as room:
        path = "sample-agent.document"

        await room.agents.invoke_tool(
            toolkit="meshagent.document-writer",
            tool="run_meshagent.document-writer_task",
            input={
                "path": path,
                "prompt": "write a paragraph about ai and how agents are shaping the future",
            },
        )
        project_id = os.getenv("MESHAGENT_PROJECT_ID")
        if project_id:
            print(
                f"Take a look at it at https://studio.meshagent.com/projects/{project_id}/rooms/{room.room_name}?p={path}"
            )


asyncio.run(main())
