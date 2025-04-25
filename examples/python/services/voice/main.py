from meshagent.agents.hosting import RemoteAgentServer
import asyncio
import os
from meshagent.livekit.agents.voice import Voice

class SampleVoiceAgent(Voice):
    def __init__(self):
        super().__init__(
            name="meshagent.livekit.agent",
            title="sample voice agent",
            description="sample agent that will respond to a query via voice",
            labels=[ "voice" ],
            auto_greet_prompt="hello",
            rules=[
                "You are a helpful assistant communicating through voice."
            ]
        )

async def server():

    remote_agent_server = RemoteAgentServer(
        cls=SampleVoiceAgent,
        path="/webhook",
        validate_webhook_secret=False,
        port=int(os.getenv("MESHAGENT_PORT"))
    )
    await remote_agent_server.run()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(server())