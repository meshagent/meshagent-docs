import asyncio

# We'll use pydantic to automate the creation of our input schemas.
from meshagent.tools.pydantic import BaseModel, PydanticTool
from meshagent.tools import ToolContext, Toolkit, connect_remote_toolkit


# define the structure of the input of our agent
class Input(BaseModel):
    # We are using "strict" mode in our LLM, so we need to forbid extra properties
    model_config = dict(extra="forbid")
    a: int
    b: int


class Adder(PydanticTool):
    def __init__(self):
        super().__init__(
            name="adder",
            title="sample adder",
            description="an agent that adds two numbers",
            input_model=Input,
        )

    # Our agent will receive content matching the input format, and must return content matching the output format
    async def execute_model(self, context: ToolContext, arguments: Input):
        result = {"result": arguments.a + arguments.b}
        print(result)
        return result


async def main():
    room_name = "examples"

    # start our agent in developer mode, it will connect to the room and be available immediately from the admin console UI
    await connect_remote_toolkit(
        room_name=room_name,
        toolkit=Toolkit(
            name="samples.adder-tool",
            title="adder",
            description="a tool that can add two numbers",
            tools=[Adder()],
        ),
    )


asyncio.run(main())
