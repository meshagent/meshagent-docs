# meshagent room connect --room=my-room --identity=sample-participant -- python3 llm-proxy-openai-sdk.py

import os
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["OPENAI_API_KEY"],
)

response = client.responses.create(
    model="gpt-5.4",
    input="Tell me a fun fact about AI.",
)

print(response.output_text)
