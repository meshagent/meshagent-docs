import os
import asyncio
import logging
import argparse
from meshagent.api import RoomClient
import pyarrow as pa
from meshagent.otel import otel_config

otel_config(service_name="resume-runner")
log = logging.getLogger("resume-runner")


async def create_resume_tables(room_name):
    # Run with:
    # meshagent room connect --room=resume --identity=participant -- python3 setup_tables.py
    async with RoomClient() as room:
        tables = await room.datasets.list_tables()
        log.info("Existing tables: %s", tables)
        # await room.datasets.drop_table(name="candidates") #remove later
        try:
            await room.datasets.create_table_with_schema(
                name="candidates",
                schema={
                    "resume_path": pa.string(),
                    "candidate_first_name": pa.string(),
                    "candidate_last_name": pa.string(),
                    "candidate_email": pa.string(),
                    "candidate_phone_number": pa.string(),
                    "resume_summary": pa.string(),
                    "web_search_notes": pa.string(),
                },
                mode="create_if_not_exists",
            )
            log.info("candidates table created if it did not already exist")
        except Exception as e:
            log.exception(f"Failed to create candidates table: {e}")

        # await room.datasets.drop_table(name="open_roles") #remove later
        try:
            await room.datasets.create_table_with_schema(
                name="open_roles",
                schema={
                    "hiring_manager_first_name": pa.string(),
                    "hiring_manager_last_name": pa.string(),
                    "job_title": pa.string(),
                    "job_description": pa.string(),
                    "required_skills": pa.string(),
                    # "post_date": pa.string()
                },
                mode="create_if_not_exists",
            )
            log.info("open_roles table created if it did not already exist")
        except Exception as e:
            log.exception(f"Failed to create open_roles table: {e}")

        # await room.datasets.drop_table(name="candidate_role_scores") #remove later
        try:
            await room.datasets.create_table_with_schema(
                name="candidate_role_scores",
                schema={
                    "candidate_first_name": pa.string(),
                    "candidate_last_name": pa.string(),
                    "candidate_email": pa.string(),
                    "hiring_manager": pa.string(),
                    "job_title": pa.string(),
                    "score": pa.float64(),
                    "reasoning": pa.string(),
                },
                mode="create_if_not_exists",
            )
            log.info("candidate_role_scores table created if it did not already exist")
        except Exception as e:
            log.exception(f"Failed to create candidate_role_scores table: {e}")


parser = argparse.ArgumentParser()
parser.add_argument("--room", default=os.getenv("ROOM_NAME", "resume"))
args = parser.parse_args()

asyncio.run(create_resume_tables(room_name=args.room))
# python3 setup_tables.py --room resume
