import 'package:meshagent/meshagent.dart';

void main() async {
  // Instantiate a new RoomClient for interacting with the room
  final room = RoomClient(
    protocol: WebSocketClientProtocol(url: Uri.parse("..."), token: "..."),
  );

  // Connect to the room
  await room.start();
}
