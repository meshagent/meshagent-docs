import asyncio

# We'll use pydantic to automate the creation of our input and output schemas.
from meshagent.agents.pydantic import PydanticAgent, BaseModel
from meshagent.agents import AgentCallContext, RemoteTaskRunnerServer

# define the structure of the input of our agent
class Input(BaseModel):
    model_config = dict(extra="forbid")
    a: int
    b: int

# define the structure of the output of our agent
class Output(BaseModel):
    model_config = dict(extra="forbid")
    result: int

class Adder(PydanticAgent):
    def __init__(self):
        super().__init__(
            name="samples.adder",
            title="sample adder",
            description="an agent that adds two numbers",
            input_model=Input,
            output_model=Output,
        )

    # Our agent will receive content matching the input format, and must return content matching the output format
    async def ask_model(self, context: AgentCallContext, arguments: Input) -> Output:        
        return Output(result=arguments.a + arguments.b)


async def main():    
    server = RemoteTaskRunnerServer(cls=Adder)
    await server.run()

if __name__ == '__main__':
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(main())
    
