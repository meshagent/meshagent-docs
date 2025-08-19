import { RoomClient, websocketProtocol } from "@meshagent/meshagent";

async function main() {
    try {
        // Define a unique room name and chose your participant name
        const roomName = "my-room";
        const participantName = "participant-name";

        // Document name (the extension identifies the schema)
        const path = "hello-world.document";

        // Establish communication channel using participant token
        const protocol = await websocketProtocol({
            roomName,
            participantName,
        });

        // Instantiate a new RoomClient for interacting with the room
        const room = new RoomClient({protocol});

        // Connect to the room
        await room.start();

        // Open our document
        const meshDocument = await room.sync.open(path);

        // Wait for the document to sync from the server
        await meshDocument.synchronized;

        // Append body with text
        meshDocument.root.createChildElement("body", {
            text: "hello world!"
        });

        // sleep 2 seconds
        await new Promise((resolve) => setTimeout(resolve, 2000));

        // Close the document 
        await room.sync.close(path);

    } catch (error) {
        console.error("Error:", error);
    }
}

main();

