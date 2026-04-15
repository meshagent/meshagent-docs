import 'package:meshagent/meshagent.dart';
import 'package:meshagent/helpers.dart' show websocketProtocol;

void main() async {
  // Define a unique room name and chose your participant name
  const String roomName = 'examples';
  const String participantName = 'example-participant';

  // Document name (the extension identifies the schema)
  const String path = 'hello-world.document';

  // Establish communication channel using participant token
  final protocolFactory = websocketProtocol(
    roomName: roomName,
    participantName: participantName,
  );

  // Instantiate a new RoomClient for interacting with the room
  final room = RoomClient(protocolFactory: protocolFactory);

  // Connect to the room
  await room.start();

  // Open our document
  final meshDocument = await room.sync.open(path);

  // Wait for the document to sync from the server
  await meshDocument.synchronized;

  meshDocument.root.createChildElement("body", {"text": "hello world!"});
}
