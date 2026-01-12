import asyncio
from meshagent.api.services import ServiceHost
from meshagent.livekit.agents.voice import VoiceBot
from meshagent.otel import otel_config

service = ServiceHost()

otel_config(service_name="simple-voicebot")  # enable telemetry for this service

@service.path(path="/voice", identity="simple-voicebot")
class SimpleVoiceBot(VoiceBot):
    def __init__(self):
        super().__init__(
            name="simple-voicebot",
            title="Simple VoiceBot",
            description="A voice assistant",
            rules=[
                "Be concise and friendly.",
                "End each reply with a short fun fact.",
            ],
            auto_greet_message="Hi! I'm your voice assistant—ask me anything.",
        )

asyncio.run(service.run())
