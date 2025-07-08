import asyncio

# We'll use pydantic to automate the creation of our input and output schemas.
from meshagent.agents.pydantic import PydanticWriter, BaseModel, WriterContext
from meshagent.agents import connect_development_agent


# define the structure of the input of our agent
class Input(BaseModel):
    model_config = dict(extra="forbid")
    # input must contain a path property, the base writer will write to the document at the specified path
    path: str
    content: str


# define the structure of the output of our agent
class Output(BaseModel):
    model_config = dict(extra="forbid")
    content: str


class SampleWriter(PydanticWriter):
    def __init__(self):
        super().__init__(
            name="samples.writer",
            title="sample writer",
            description="a agent that writes to a document",
            input_model=Input,
            output_model=Output,
        )

    # Our writer agent will receive a copy of the document. Any changes we make to the document will be automatically
    # saved and synchronized to other participants in the room.
    async def write_model(
        self, writer_context: WriterContext, arguments: Input
    ) -> Output:
        print(f"writing content {arguments.content}")
        writer_context.document.root.append_child(
            tag_name="body", attributes={"text": arguments.content}
        )
        return Output(content="success")


async def main():
    room_name = "examples"

    # start our agent in developer mode, it will connect to the room and be available immediately from the admin console UI
    await connect_development_agent(room_name=room_name, agent=SampleWriter())


asyncio.run(main())
