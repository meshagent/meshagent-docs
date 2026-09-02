# python3 llm-proxy-langchain.py

import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-5.4",
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["OPENAI_API_KEY"],
    default_headers={"Meshagent-Project-Id": os.environ["MESHAGENT_PROJECT_ID"]},
)

result = llm.invoke("Tell me a fun fact about AI.")
print(result.content)
