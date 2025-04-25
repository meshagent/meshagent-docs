from meshagent.api import RequiredToolkit
from meshagent.agents.hosting import RemoteAgentServer
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.computers import ComputerAgent, BrowserbaseBrowser, Operator

import asyncio
import os

class BrowserbaseAgent(ComputerAgent):
    def __init__(self): 
        super().__init__(
            name="meshagent.browser",
            title="browser agent",
            description="a task runner that can use a browser",
            requires=[
                RequiredToolkit(
                    name="ui",
                    tools=[
                        #"ask_user",
                        #"display_document",
                        #"show_toast"
                    ]
                ),
            ],
            llm_adapter = OpenAIResponsesAdapter(
                model="computer-use-preview",
                response_options={
                    "reasoning" : {
                        "generate_summary" : "concise"
                    },
                    "truncation" : "auto"
                }
            ),

            labels=[ "tasks", "computers" ],
            computer_cls=BrowserbaseBrowser,
            operator_cls=Operator
        )

async def server():

    remote_agent_server = RemoteAgentServer(
        cls=BrowserbaseAgent,
        path="/webhook",
        validate_webhook_secret=False,
        port=int(os.getenv("MESHAGENT_PORT"))
    )
    await remote_agent_server.run()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(server())