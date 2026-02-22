import asyncio
import os
from meshagent.api import (
    RoomClient,
    ParticipantToken,
    WebSocketClientProtocol,
    websocket_room_url,
)


async def main():
    room_name = "quickstart"

    # a participant token says who this participant is and what they are allowed to do.
    # Make sure your API secret in the MESHAGENT_SECRET environment variable.
    # This secret will be used to sign the token so that the server knows that the token is valid.
    token = ParticipantToken(
        name="my user",
        project_id=os.getenv("MESHAGENT_PROJECT_ID"),
        api_key_id=os.getenv("MESHAGENT_KEY_ID"),
    )

    token.add_room_grant(room_name=room_name)

    # connect to the room, it will automatically be created if it does not exist yet.
    # We'll establish a connection to the server using a websocket.
    url = websocket_room_url(room_name=room_name)

    async with RoomClient(
        protocol=WebSocketClientProtocol(
            url=url, token=token.to_jwt(token=os.getenv("MESHAGENT_SECRET"))
        )
    ) as room:
        path = "sample-agent.document"

        # Invoke the TaskRunner tool to write content to the document.
        # The document will automatically be created if it does not already exist.

        await room.agents.invoke_tool(
            toolkit="meshagent.document-writer",
            tool="run_meshagent.document-writer_task",
            input={
                "path": path,
                "prompt": "write a paragraph about ai and how agents are shaping the future",
            },
        )
        print(
            f"Take a look at it at https://studio.meshagent.com/projects/{os.getenv('MESHAGENT_PROJECT_ID')}/rooms/{room_name}?p={path}"
        )


asyncio.run(main())
