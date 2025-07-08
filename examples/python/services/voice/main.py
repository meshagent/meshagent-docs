from meshagent.livekit.agents.voice import VoiceBot
from meshagent.api.services import ServiceHost

import asyncio

service = ServiceHost()


@service.path("/agent")
class SampleVoiceAgent(VoiceBot):
    def __init__(self):
        super().__init__(
            name="meshagent.livekit.agent",
            title="sample voice agent",
            description="sample agent that will respond to a query via voice",
            labels=["voice"],
            auto_greet_prompt="hello",
            rules=["You are a helpful assistant communicating through voice."],
        )


asyncio.run(service.run())
