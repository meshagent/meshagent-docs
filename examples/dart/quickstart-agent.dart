import 'package:meshagent/meshagent.dart';
import 'package:meshagent/helpers.dart' show websocketProtocol;

Future<void> main() async {
  const roomName = 'quickstart';
  const participantName = 'my-user';
  const path = 'sample-agent.document';

  final protocolFactory = websocketProtocol(
    roomName: roomName,
    participantName: participantName,
  );
  final room = RoomClient(protocolFactory: protocolFactory);

  try {
    await room.start();

    await room.agents.call(
      name: 'meshagent.document-writer',
      url: 'https://api.meshagent.life/agents/meshagent.document-writer',
      arguments: const {},
    );

    await room.agents.invokeTool(
      toolkit: 'meshagent.document-writer',
      tool: 'run_meshagent.document-writer_task',
      input: ToolContentInput(
        JsonContent(
          json: {
            'path': path,
            'prompt':
                'write a paragraph about AI and how agents are shaping the future',
          },
        ),
      ),
    );

    print('Take a look at it in MeshAgent Studio.');
  } finally {
    room.dispose();
  }
}
