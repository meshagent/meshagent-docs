import asyncio
import os
from meshagent.api import RoomClient


async def main():
    # Run with:
    # meshagent room connect --room=quickstart --identity=my-user -- python3 quickstart-document.py
    async with RoomClient() as room:
        path = "sample.document"
        document = await room.sync.open(path=path, create=True)
        try:
            await document.synchronized
            document.root.append_child(
                tag_name="body", attributes={"text": "hello world!"}
            )
        finally:
            # make sure to cleanup the document connection when we are done with it
            await room.sync.close(path=path)

        project_id = os.getenv("MESHAGENT_PROJECT_ID")
        if project_id:
            print(
                f"Take a look at it at https://studio.meshagent.com/projects/{project_id}/rooms/{room.room_name}?p={path}"
            )


asyncio.run(main())
