import os
import asyncio
import logging
from meshagent.api import ParticipantToken, ApiScope, RoomClient, WebSocketClientProtocol, ParticipantGrant
from meshagent.api.room_server_client import TextDataType, FloatDataType
from meshagent.otel import otel_config

otel_config(service_name="resume-runner")
log = logging.getLogger("resume-runner")

def env(name: str) -> str:
    val = os.getenv(name)
    if not isinstance(val, str) or not val:
        raise RuntimeError(f"Missing required environment variable: {name}.")
    return val

async def create_resume_tables(room_name):
    api_key=env("MESHAGENT_API_KEY")
    async with RoomClient(
        protocol=WebSocketClientProtocol(
            url=f"wss://api.meshagent.com/rooms/{room_name}",
            token=ParticipantToken(
                name="participant",
                grants=[
                    ParticipantGrant(name="room", scope=room_name),
                    ParticipantGrant(name="role", scope="agent"),
                    ParticipantGrant(name="api", scope=ApiScope.agent_default()),
                ]
            ).to_jwt(api_key=api_key)
        )
    ) as room:
        tables = await room.database.list_tables()
        log.info("Existing tables: %s", tables)

        await room.database.drop_table(name="candidates", ignore_missing=True) # remove later
        try: 
            await room.database.create_table_with_schema(
                name="candidates",
                schema={
                    "candidate_id": TextDataType(),
                    "resume_path": TextDataType(),
                    "candidate_name": TextDataType(),
                    "contact_info": TextDataType(),
                    "resume_text": TextDataType(),
                    "resume_summary": TextDataType(), 
                    "web_search_notes": TextDataType()
                },
                mode="create_if_not_exists"
            )
            log.info("candidates table created if it did not already exist")
        except Exception as e:
            log.exception(f"Failed to create candidates table: {e}")

        try:
            await room.database.create_table_with_schema(
                name="open_roles",
                schema={
                    "role_id": TextDataType(),
                    "hiring_manager": TextDataType(),
                    "title": TextDataType(),
                    "job_description_path": TextDataType(),
                    "required_skills": TextDataType(),
                },
                mode="create_if_not_exists",
            )
            log.info("open_roles table created if it did not already exist")
        except Exception as e:
            log.exception(f"Failed to create open_roles table: {e}")
        
        try:
            await room.database.create_table_with_schema(
                name="candidate_role_scores",
                schema={
                    "candidate_id": TextDataType(),
                    "role_id": TextDataType(),
                    "score": FloatDataType(),
                    "reasoning": TextDataType()
                },
                mode="create_if_not_exists"
            )
            log.info("candidate_role_scores table created if it did not already exist")
        except Exception as e:
            log.exception(f"Failed to create candidate_role_scores table: {e}")

asyncio.run(create_resume_tables(room_name="resume"))
