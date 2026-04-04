import { RoomClient, websocketProtocol } from "@meshagent/meshagent";

async function main() {
    try {
        // Define a unique room name and chose your participant name
        const roomName = "my-room";
        const participantName = "participant-name";

        // Initialize the communication protocol
        const protocol = await websocketProtocol({roomName, participantName});

        // Instantiate a new RoomClient for interacting with the room
        const room = new RoomClient({protocol});

        // Connect to the room
        await room.start();

        const data = new TextEncoder().encode("Hello, Storage!");
        if (!(await room.storage.exists("example.txt"))) {
            await room.storage.upload("example.txt", data, { overwrite: true });
        }

        const response = await room.storage.download("example.txt");
        console.log("Downloaded content:", new TextDecoder().decode(response.data));

        await room.storage.delete("example.txt");

        room.dispose();

    } catch (error) {
        console.error("Error starting the room client:", error);
    }
}
main();
