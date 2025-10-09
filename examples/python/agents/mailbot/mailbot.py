import asyncio
from meshagent.otel import otel_config
from meshagent.api import Meshagent
from meshagent.api.services import ServiceHost
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.agents.mail import MailWorker 

# Enable OpenTelemetry logging and tracing for the agent 
otel_config(service_name="mailbot")

# Create/allocate an email for the agent with MeshAgent

# Create a service host
service = ServiceHost() # optional to pass a port, MeshAgent automatically assigns an available one if none provided

# Register an agent at a specific path
@service.path(path="/mail", identity="mailbot")
class ExampleMailbot(MailWorker):
    def __init__(self):
        super().__init__(
            name="mailbot",
            title="mailbot",
            description="An agent that responds via email",
            llm_adapter=OpenAIResponsesAdapter(),
            rules=["You are a helpful asssistant that responds to users via email."],
            queue="email",
            email_address="example@mail.meshagent.life"
        )

asyncio.run(service.run())