import asyncio
from meshagent.api import RoomClient, websocket_protocol

async def run_schema_planner(room_name:str, prompt:str, output_schema:dict, participant_name:str="test_user"):
    """
    Run the Planner in a MeshAgent Room

    Args:
        room_name: Name of the room to connect to
        prompt: The user prompt to send to the agent
        output_schema: The structured output to use in the response 
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
                agent="meshagent.schema_planner",
                arguments={
                    "prompt": prompt,
                    "output_schema": output_schema
                }
            )
            return response
    except Exception as e:
        print(f"Connection failed: {e}")

product_schema = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "title": {"type": "string"},
        "price": {"type": "number"},
        "features": {"type": "array", "items": {"type": "string"}},
        "description": {"type": "string"}
    },
    "required": ["title", "price", "features", "description"]
}

asyncio.run(run_schema_planner(room_name="test", prompt="Create a product listing for a bluetooth speaker", output_schema=product_schema))