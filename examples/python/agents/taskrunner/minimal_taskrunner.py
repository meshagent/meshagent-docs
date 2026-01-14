import asyncio
from meshagent.api.services import ServiceHost
from meshagent.agents import TaskRunner, AgentCallContext

service = ServiceHost()


@service.path(path="/task", identity="hello-taskrunner")
class HelloTask(TaskRunner):
    def __init__(self):
        super().__init__(
            name="hello-taskrunner",
            title="Hello Task",
            description="Returns a friendly greeting.",
            input_schema=None,  # defaults to no-args schema
            output_schema={
                "type": "object",
                "properties": {"result": {"type": "string"}},
                "required": ["result"],
            },
        )

    async def ask(self, *, context: AgentCallContext, arguments: dict) -> dict:
        return {"result": "Hello from TaskRunner!"}


asyncio.run(service.run())
