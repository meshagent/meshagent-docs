import asyncio
from meshagent.api.services import ServiceHost
from meshagent.tools import Tool, ToolContext, RemoteToolkit
from meshagent.otel import otel_config

otel_config(service_name="math_tools")
service = ServiceHost()


class Add(Tool):
    def __init__(self):
        super().__init__(
            name="add",
            title="adding tool",
            description="a tool that adds two numbers",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["a", "b"],
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"},
                },
            },
        )

    async def execute(self, context: ToolContext, *, a: int, b: int):
        result = {"result": a + b}
        print(result)
        return result


class Subtract(Tool):
    def __init__(self):
        super().__init__(
            name="subtract",
            title="subtracting tool",
            description="a tool that subtracts two numbers",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["a", "b"],
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"},
                },
            },
        )

    async def execute(self, context: ToolContext, *, a: int, b: int):
        result = {"result": a - b}
        print(result)
        return result


@service.path(path="/math", identity="math-toolkit")
class MathToolkit(RemoteToolkit):
    def __init__(self):
        super().__init__(
            name="math-toolkit",
            title="math-toolkit",
            description="a toolkit for adding and subtracting numbers",
            tools=[Add(), Subtract()],
        )


if __name__ == "main":
    print(f"running on port {service.port}")
    asyncio.run(service.run())
