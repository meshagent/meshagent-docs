import asyncio
import os
from meshagent.api import (
    RoomClient,
    ParticipantToken,
    WebSocketClientProtocol,
    websocket_room_url,
)


# We'll define an async function that runs a client as "Alice" or "Bob"
async def run_participant(participant_name: str):
    """
    Connects to a MeshAgent room under the given participant name,
    enables messaging, and returns the connected room object.
    """
    room_name = "example_room"

    # 1. Create a participant token for this user.
    #    We'll assume we have environment variables for the Project ID, Key ID, and Secret.
    token = ParticipantToken(
        name=participant_name,
        project_id=os.getenv("MESHAGENT_PROJECT_ID"),
        api_key_id=os.getenv("MESHAGENT_KEY_ID"),
    )
    # Add a grant for the room so this participant can connect.
    token.add_room_grant(room_name=room_name)

    # 2. Build a signed token using our MESHAGENT_SECRET.
    jwt = token.to_jwt(token=os.getenv("MESHAGENT_SECRET"))

    # 3. Build the WebSocket URL to connect to the specified room.
    url = websocket_room_url(room_name=room_name)

    # 4. Create a RoomClient with the WebSocket protocol.
    room = RoomClient(protocol=WebSocketClientProtocol(url=url, token=jwt))

    # 5. We'll open (enter) the connection.
    await room.__aenter__()  # same as "async with room"
    # Wait for the server to signal "room_ready", so we know we’re connected.
    # Then we also start up the synchronization logic, etc.

    # 6. Enable messaging
    await room.messaging.enable()

    print(f"[{participant_name}] connected and messaging enabled.")

    # 7. We'll define a handler for incoming messages
    def on_message(message):
        print(
            f"[{participant_name}] RECEIVED a message from {message.from_participant_id} with type '{message.type}': {message.message}"
        )

    room.messaging.on("message", on_message)

    return room


async def main():
    # 1. Start "Alice" participant
    alice_room = await run_participant("Alice")
    # 2. Start "Bob" participant
    bob_room = await run_participant("Bob")

    # At this point, both are connected to the same room.
    # The server has assigned them each an ID.
    # We can find Bob's remote participant object from Alice's perspective
    # but we need to give the server a moment to propagate Bob’s presence.
    await asyncio.sleep(1.0)

    # Let's find Bob in Alice's room:
    # (in a real-world scenario, you might identify him by a known attribute or ID)
    bob_participant = None
    for p in alice_room.messaging.remote_participants:
        if p.get_attribute("name") == "Bob":
            bob_participant = p
            break

    if bob_participant is None:
        print("Alice can't find Bob yet, try again later or ensure Bob is discovered.")
    else:
        # 3. Alice sends a message to Bob
        await alice_room.messaging.send_message(
            to=bob_participant,
            type="hello_bob",
            message={"text": "Hi Bob, how are you?"},
        )
        print("[Alice] Sent a message to Bob.")

    # Bob also sees participants. We do the same from Bob's perspective to find Alice.
    await asyncio.sleep(1.0)
    alice_participant = None
    for p in bob_room.messaging.remote_participants:
        if p.get_attribute("name") == "Alice":
            alice_participant = p
            break

    if alice_participant:
        # 4. Bob replies back
        await bob_room.messaging.send_message(
            to=alice_participant,
            type="hello_alice",
            message={"text": "Hello Alice, I'm doing great!"},
        )
        print("[Bob] Replied to Alice.")

    # We'll keep the connections alive for a few seconds so logs can be printed
    await asyncio.sleep(3.0)

    # Finally, clean up
    await alice_room.__aexit__(None, None, None)
    await bob_room.__aexit__(None, None, None)
    print("Exiting.")


asyncio.run(main())
