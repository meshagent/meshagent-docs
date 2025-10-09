import 'package:meshagent/meshagent.dart';

void main() async {
  // Instantiate a new RoomClient for interacting with the room
  final roomName = "my-room";
  final participantName = "participant-name";
  final apiKey = String.fromEnvironment('MESHAGENT_API_KEY', defaultValue: "");
  final token = ParticipantToken(name: participantName);
  token.addRoomGrant(roomName);
  token.addRoleGrant("agent");
  token.addApiGrant(ApiScope.agentDefault());

  final protocol = WebSocketClientProtocol(
    url: Uri.parse("wss://api.meshagent.com/rooms/$roomName"),
    token: token.toJwt(apiKey: apiKey),
  );

  final room = RoomClient(protocol: protocol);

  // Connect to the room
  await room.start();
}
