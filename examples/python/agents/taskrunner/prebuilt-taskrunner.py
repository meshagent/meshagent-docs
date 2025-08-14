import asyncio
from meshagent.api import RoomClient, websocket_protocol

async def run_planner(room_name:str, prompt:str, participant_name:str="test_user"):
    """
    Run the Planner in a MeshAgent Room

    Args:
        room_name: Name of the room to connect to
        prompt: The user prompt to send to the agent 
        participant_name: Name to use as participant (defaults to "test_user")
    """
    try:
        async with RoomClient(
            protocol=websocket_protocol(
                participant_name=participant_name, 
                room_name=room_name
            )
        ) as room:
            response = await room.agents.ask(
                agent="meshagent.planner",
                arguments={
                    "prompt": prompt
                    }
                )
            return response
    except Exception as e:
        print(f"Connection failed: {e}")

asyncio.run(run_planner(room_name="test", prompt="Write a product description for a bluetooth speaker"))
