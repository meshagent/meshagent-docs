import os
import asyncio
import logging
from meshagent.agents.chat import ChatBot
from meshagent.api.services import ServiceHost
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.otel import otel_config

# Enable OpenTelemetry logging and tracing for the agent
otel_config(service_name="chatbot-service")
log = logging.getLogger("chatbot-service")

# Pass a system prompt, custom rules / instructions, that you want the agent to follow.
system_prompt = os.getenv("SYSTEM_PROMPT")
rules = [system_prompt] if system_prompt else []
# print(f"starting service with rule: {system_prompt}", flush=True)

# ServiceHost runs an HTTP server that exposes agents or tools as webhook endpoints and manages their lifecycle
# Port defaults to an available port if not assigned
host = ServiceHost()

# Register an agent with the host. The @host.path decorator maps the
# endpoint "/agent" to this agent class. When the host receives a
# “room.call” webhook on that path, it will spawn an instance of
# MyChatBot and connect it to the calling room.


@host.path(path="/agent", identity="chatbot")
class MyChatBot(ChatBot):
    # ChatBot is a conversational, text-based agent that maintains context of the conversation and routes messages to a language model
    def __init__(self):
        super().__init__(
            name="chatbot",
            rules=rules,
            llm_adapter=OpenAIResponsesAdapter(),  # Connect to an OpenAI model that uses the Responses API (e.g. GPT 4.1, o3)
        )


# Run the host. It starts listening for webhook calls and gracefully
# shuts down when the process receives a termination signal.
asyncio.run(host.run())
