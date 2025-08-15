import os
import json
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

async def talk_to_agent():
    room_name = "mynewroomtest"
    try:
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
            await room.messaging.enable() # turn on messaging 
            participants = room.messaging.get_participants()
            participant_names = [p.get_attribute("name") for p in participants]
            log.info(f"Available participants: {participant_names}")

            chatbot = None
            for p in participants:
                if p.get_attribute("name") == "chatbot":
                    chatbot = p
                    break

            if not chatbot:
                log.info("No participant named 'chatbot' is present.")
                return

            log.info("Sending chatbot a message")
            response = await room.messaging.send_message(
                to=chatbot,
                type="chat",
                message={"prompt": "Hello, who are you?"}
            )
            print(f"Response: {response}")   # prints the agent's reply
            log.info(f"Response: {response}")


    except Exception as e:
        print(f"Error communicating with agent: {e}")

asyncio.run(talk_to_agent())
