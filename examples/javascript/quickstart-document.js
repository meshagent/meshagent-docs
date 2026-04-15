import { RoomClient } from "@meshagent/meshagent";

// Run with:
// meshagent room connect --room=quickstart --identity=my-user -- <your node command>

async function main() {
    const path = "sample.document";
    const room = new RoomClient();

    try {
        await room.start();
        const document = await room.sync.open(path, { create: true });
        try {
            await document.synchronized;
            document.root.createChildElement("body", { text: "hello world!" });
        } finally {
            await room.sync.close(path);
        }

        const projectId = process.env.MESHAGENT_PROJECT_ID;
        if (projectId != null && projectId.length > 0) {
            console.log(
                `Take a look at it at https://studio.meshagent.com/projects/${projectId}/rooms/${room.roomName}?p=${path}`,
            );
        }
    } catch (error) {
        console.error("Error:", error);
    } finally {
        room.dispose();
    }
}

void main();
