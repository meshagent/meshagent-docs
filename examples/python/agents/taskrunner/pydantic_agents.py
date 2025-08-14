import os
import json
import asyncio
import logging
from datetime import date, datetime
from meshagent.otel import otel_config
from meshagent.api.services import ServiceHost
from meshagent.agents import TaskRunner

from pydantic_ai import Agent
from pydantic import BaseModel, Field, ConfigDict
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

otel_config(service_name="my-service")

service = ServiceHost(
    port=int(os.getenv("MESHAGENT_PORT","7777")) # if you don't pass a port it defaults to 8081
)

# Define Inputs, Outputs, and Pydantic AI Agent for Translation
class TranslationInput(BaseModel):
    text:str = Field(..., description="Text to translate")
    model_config = ConfigDict(extra='forbid')

class TranslationResult(BaseModel):
    french_translation:str
    spanish_translation:str
    model_config = ConfigDict(extra='forbid')

translation_agent = Agent(
    model=AnthropicModel('claude-4-sonnet-20250514', provider=AnthropicProvider()), #pass API key from env variables
    deps_type=None,
    instructions=f"""
        # Role Background
        You are responsible for translating recent news announcements into other languages. You are exposed to a variety of topics beyond your knowledge cutoff date. The current date is: {date.today().strftime("%B %d, %Y")}

        # Task
        Provide two translations, one in French and one in Spanish.     
    """,
    output_type=TranslationResult
)

# Utility function
async def save_to_storage(room, path: str, data: bytes):
        handle = await room.storage.open(path=path, overwrite=True)
        await room.storage.write(handle=handle, data=data)
        await room.storage.close(handle=handle)

# Use Pydantic AI agent in a MeshAgent Room
@service.path("/translator")
class TranslationTaskRunner(TaskRunner):
    def __init__(self):
        super().__init__(
            name="translator",
            description="An agent that translates text to French and Spanish",
            input_schema=TranslationInput.model_json_schema(),
            output_schema=TranslationResult.model_json_schema()
        )

    async def ask(self, *, context, arguments):
        room=context.room

        inputs = TranslationInput(**arguments)
        log.info(f"Translating Text: {inputs.text}")

        translations = await translation_agent.run(inputs.text)
        log.info(f"Translation Result: {translations.output}")

        # save results to room storage
        log.info(f"Translation completed, writing raw results to Room storage.")
        
        await save_to_storage(
            room=room,
            path=f"translations/{room.room_name}-translation-{datetime.now():%Y%m%dT%H%M%S}.json",
            data=json.dumps({"input_text": inputs.text, "translations": translations.output.model_dump()}, indent=2, ensure_ascii=False).encode("utf-8")
        )

        return translations.output.model_dump()

print(f"running on port {service.port}")
asyncio.run(service.run())