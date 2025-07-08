from meshagent.api import RequiredToolkit
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.computers import ComputerAgent, BrowserbaseBrowser, Operator
from meshagent.api.services import ServiceHost

import asyncio

service = ServiceHost()

@service.path("/agent")
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


asyncio.run(service.run())