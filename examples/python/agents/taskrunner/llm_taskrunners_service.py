import os
import asyncio
import logging
# either import from other file or add this code to your existing file that defines the LLMTaskRunners
from llm_taskrunner import LLMTaskRunner, DynamicLLMTaskRunner
from meshagent.otel import otel_config
from meshagent.api.services import ServiceHost
from meshagent.openai import OpenAIResponsesAdapter

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

otel_config(service_name="llm-taskrunner")
service = ServiceHost(port=int(os.getenv("MESHAGENT_PORT", "7777")))

@service.path("/llmtaskrunner")
class LLMRunner(LLMTaskRunner):
    def __init__(self):
        super().__init__(
            name="llmtaskrunner",
            title="LLM Task Runner",
            description="Returns {result: string} unless overridden.",
            llm_adapter=OpenAIResponsesAdapter(),
            toolkits=None,
            supports_tools=True,
            input_prompt=True,
            output_schema={
                "type": "object",
                "required": ["result"],
                "additionalProperties": False,
                "properties": {"result": {"type": "string"}},
            }
        )

@service.path("/dynamicllmtaskrunner")
class DynamicLLMRunner(DynamicLLMTaskRunner):
    def __init__(self):
        super().__init__(
            name="dynamicllmtaskrunner",
            title="Dynamic LLM TaskRunner",
            description="Prompt + caller‑supplied JSON Schema → structured output.",
            llm_adapter=OpenAIResponsesAdapter(),
        )

print(f"Running on port {service.port}")
asyncio.run(service.run())
