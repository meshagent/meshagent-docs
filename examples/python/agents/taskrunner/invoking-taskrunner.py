import asyncio
import json
from typing import Dict, Any
from meshagent.api import RoomClient, websocket_protocol

async def call_agent(
    room_name: str, 
    agent_name: str, 
    arguments: Dict[str, Any], 
    participant_name: str = "api_client"
) -> Dict[str, Any]:
    """Call a MeshAgent agent with the given arguments."""
    async with RoomClient(
        protocol=websocket_protocol(
            participant_name=participant_name, 
            room_name=room_name
        )
    ) as room:
        result = await room.agents.ask(
            agent=agent_name, 
            arguments=arguments
        )
        # Extract JSON data from JsonBody response
        return result.json if hasattr(result, 'json') else result

async def main():
    # Call your translator
    result = await call_agent(
        room_name="translate",
        agent_name="translator",
        arguments={"text": "Hello, how are you today?"}
    )
    
    print("Translation result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
