import asyncio,json
from pathlib import Path
from meshagent.api.client import Meshagent

SESSION = Path("~/.meshagent/session.json").expanduser()
tokens = json.loads(SESSION.read_text())
access_token = tokens["access_token"]

async def main():
    client = Meshagent(token=access_token) 
    try:
        projects = await client.list_projects()
        print(projects)
    finally:
        await client.close()

asyncio.run(main())