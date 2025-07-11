import asyncio

# We'll use pydantic to automate the creation of our input and output schemas.
from meshagent.agents.pydantic import PydanticAgent, BaseModel
from meshagent.agents import AgentCallContext, connect_development_agent


# define the structure of the input of our agent
class Input(BaseModel):
    model_config = dict(extra="forbid")


# define the structure of the output of our agent
class Output(BaseModel):
    model_config = dict(extra="forbid")
    result: float


class Adder(PydanticAgent):
    def __init__(self):
        super().__init__(
            name="samples.tool-adder",
            title="sample adder",
            description="an agent that adds two numbers",
            input_model=Input,
            output_model=Output,
        )

    # Our agent will receive content matching the input format, and must return content matching the output format
    async def ask_model(self, context: AgentCallContext, arguments: Input) -> Output:
        # The studio has a few built in tools for interacting with users. we'll use the ask_user tool which presents a form
        # and waits for the user to fill it out, and then returns the results.
        response = await context.room.agents.invoke_tool(
            participant_id=context.caller.id,
            toolkit="ui",
            tool="ask_user",
            arguments={
                "subject": "I need some information",
                "description": "please give me some information",
                "form": [
                    {
                        "input": {
                            "multiline": False,
                            "name": "a",
                            "description": "input a number",
                            "default_value": "5",
                        },
                    },
                    {
                        "input": {
                            "multiline": False,
                            "name": "b",
                            "description": "input a number",
                            "default_value": "5",
                        }
                    },
                ],
            },
        )

        a = float(response["a"])
        b = float(response["b"])

        return Output(result=a + b)


async def main():
    room_name = "examples"

    # start our agent in developer mode, it will connect to the room and be available immediately from the admin console UI
    await connect_development_agent(room_name=room_name, agent=Adder())


asyncio.run(main())
