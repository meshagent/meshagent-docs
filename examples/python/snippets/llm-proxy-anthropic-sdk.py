import os
from anthropic import Anthropic

default_headers = {}
default_headers["Authorization"] = f"Bearer {os.environ['MESHAGENT_ACCESS_TOKEN']}"
project_id = os.environ.get("MESHAGENT_PROJECT_ID")
if project_id:
    default_headers["Meshagent-Project-Id"] = project_id

client = Anthropic(
    base_url=os.environ.get(
        "MESHAGENT_ANTHROPIC_BASE_URL",
        "https://api.meshagent.com/anthropic",
    ),
    api_key="meshagent",
    default_headers=default_headers,
)

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=512,
    messages=[
        {
            "role": "user",
            "content": "Tell me a fun fact about AI.",
        }
    ],
)

print(message.content[0].text)
