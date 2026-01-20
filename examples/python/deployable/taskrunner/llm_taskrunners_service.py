import asyncio
from meshagent.agents.llmrunner import LLMTaskRunner, DynamicLLMTaskRunner
from meshagent.otel import otel_config
from meshagent.api.services import ServiceHost
from meshagent.openai import OpenAIResponsesAdapter

otel_config(service_name="llm-taskrunners")
service = ServiceHost()


@service.path(path="/llmtaskrunner", identity="llmtaskrunner")
class LLMRunner(LLMTaskRunner):
    def __init__(self):
        super().__init__(
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
            },
        )


@service.path(path="/dynamicllmtaskrunner", identity="dynamicllmtaskrunner")
class DynamicLLMRunner(DynamicLLMTaskRunner):
    def __init__(self):
        super().__init__(
            title="Dynamic LLM TaskRunner",
            description="Prompt + caller‑supplied JSON Schema → structured output.",
            llm_adapter=OpenAIResponsesAdapter(),
        )


asyncio.run(service.run())
