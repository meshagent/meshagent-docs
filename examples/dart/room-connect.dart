// Define a unique room name
const String roomName = 'my-room';
const String participantName = 'my-participant';

// Establish communication channel using participant token
final channel = websocketProtocol(
  roomName: roomName,
  participantName: participantName,
);

// Initialize the communication protocol
final protocol = Protocol(channel: channel);

// Instantiate a new RoomClient for interacting with the room
final room = RoomClient(protocol: protocol);

// Connect to the room
await room.start();
