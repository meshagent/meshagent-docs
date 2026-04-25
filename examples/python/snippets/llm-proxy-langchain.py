import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-5.4",
    base_url="https://api.meshagent.com/openai/v1",
    api_key=os.environ["MESHAGENT_ACCESS_TOKEN"],
    default_headers={
        "Meshagent-Project-Id": os.environ["MESHAGENT_PROJECT_ID"],
    },
)

result = llm.invoke("Tell me a fun fact about AI.")
print(result.content)
