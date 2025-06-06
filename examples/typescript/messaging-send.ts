// run_participant.ts

import {
  RoomClient,
  ParticipantToken,
  WebSocketProtocolChannel
} from "@meshagent/meshagent"; // <-- your TypeScript port or wrapper

/**
 * Connects to a MeshAgent room under the given participant name,
 * enables messaging, and returns the connected room object.
 */
export async function runParticipant(participantName: string): Promise<RoomClient> {
  const roomName = "example_room";
  const projectId = process.env.MESHAGENT_PROJECT_ID;
  const apiKeyId = process.env.MESHAGENT_KEY_ID;
  const apiKeySecret = process.env.MESHAGENT_KEY_SECRET;

  // 1. Create a participant token for this user
  const token = new ParticipantToken({
    name: participantName,
    projectId: projectId,
    apiKeyId: apiKeyId,
  });

  // Add a grant for the room so this participant can connect
  token.addRoomGrant(roomName);

  // 2. Build a signed JWT
  const jwt = token.toJwt(apiKeySecret);

  // 3. Build the WebSocket URL
  const url = `wss://api.meshagent.com/rooms/${roomName}`;

  // 4. Create a RoomClient with the WebSocket protocol
  const room = new RoomClient({
    protocol: new WebSocketProtocolChannel(url, jwt),
  });

  // 5. "enter" the connection
  await room.enter();

  // 6. Enable messaging
  await room.messaging.enable();

  console.log(`[${participantName}] connected and messaging enabled.`);

  // 7. Define a handler for incoming messages
  room.messaging.on("message", (message) => {
    console.log(
      `[${participantName}] RECEIVED a message from ${message.fromParticipantId}` +
      ` with type '${message.type}': ${JSON.stringify(message.message)}`
    );
  });

  return room;
}

