import { RoomClient, Protocol, websocketProtocol } from '@meshagent/meshagent';

async function main() {
    try {
        const roomName = 'quickstart';
        const participantName = 'my user';

        // Document path in the MeshAgent environment
        const path = 'sample-agent.document';

        const channel = await websocketProtocol({
            roomName,
            participantName,
        });

        const room = new RoomClient({
            protocol: new Protocol({ channel }),
        });

        // Connect to the room (automatically creating it if it doesn't exist)
        await room.start();

        // Add Agents to the room
        await room.agents.call({
            name: 'meshagent.document-writer',
            url: 'https://api.meshagent.life/agents/meshagent.document-writer',
            arguments: { },
        });

        // Ask an agent to do some work in the document.
        // The "meshagent.document-writer" agent writes content to the document.
        await room.agents.ask({
            agentName: 'meshagent.document-writer',
            arguments: {
                path,
                prompt: 'write a paragraph about AI and how agents are shaping the future',
            },
        });

        console.log('Take a look at it at https://studio.meshagent.com');

        // Always disconnect when done
        await room.disconnect();

    } catch (error) {
        console.error('Error:', error);
    }
}

main();

