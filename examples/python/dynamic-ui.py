import asyncio
from meshagent.api import RequiredToolkit
from meshagent.agents import TaskRunner, connect_development_agent
from meshagent.agents.utils import generate_json
from meshagent.api.schema_util import no_arguments_schema


class Sample(TaskRunner):
    def __init__(self):
        super().__init__(
            name="ask user for json",
            input_schema=no_arguments_schema(),
            output_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["first_name", "last_name"],
                "properties": {
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                },
            },
        )

    async def ask(self, *, context, arguments):
        result = await generate_json(
            on_behalf_of=context.caller,
            requires=[RequiredToolkit(name="ui", tools=["ask_user"])],
            room=self.room,
            output_schema=self.output_schema,
        )
        print(f"The result was {result}")
        return result


async def main():
    room_name = "examples"

    # start our agent in developer mode, it will connect to the room and be available immediately from the admin console UI
    await connect_development_agent(room_name=room_name, agent=Sample())


asyncio.run(main())
