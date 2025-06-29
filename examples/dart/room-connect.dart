import 'package:meshagent/meshagent.dart';

void main() async {
    // Define a unique room name

    Meshagent.initServer();
    
    Meshagent.initClient(authorizationUrl: "");

    // Instantiate a new RoomClient for interacting with the room
    final room = RoomClient(roomName: "my-room");
    
    RoomClient.withProtocol


    // Connect to the room
    await room.start();
}
