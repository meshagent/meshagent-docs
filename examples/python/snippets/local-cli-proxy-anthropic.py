import os
from anthropic import Anthropic

client = Anthropic(
    base_url=os.environ["ANTHROPIC_BASE_URL"],
    api_key=os.environ["ANTHROPIC_API_KEY"],
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
