import argparse
import asyncio
from meshagent.api import RoomClient, websocket_protocol
from meshagent.api.room_server_client import TextDataType

parser = argparse.ArgumentParser()
parser.add_argument("--room", required=True, help="Room name (creates if missing)")
args = parser.parse_args()

async def main():
    # 1. connect as a throw-away participant → this *creates* the room if needed
    async with RoomClient(
        protocol=websocket_protocol(
            room_name=args.room,
            participant_name="room-bootstrap"
            )
    ) as room:
        print("Connected to room")

        # 2. ensure the tasks table exists
        try:
            await room.database.create_table_with_schema(
                name="tasks",
                schema={
                    "task_id": TextDataType(),
                    "taskdescription": TextDataType(),
                },
                mode="overwrite",   # change to "overwrite" if you want a clean slate each run
                data=None,
            )
            print("Created table tasks")
        except room.room_exceptions.TableExistsError:
            print("Table tasks already exists — skipped")

        print(f"Room “{args.room}” ready ✔")

if __name__ == "__main__":
    asyncio.run(main())