import asyncio
from meshagent.agents.llmrunner import LLMTaskRunner
from meshagent.otel import otel_config
from meshagent.api.services import ServiceHost
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.openai.tools.responses_adapter import WebSearchToolkitBuilder, LocalShellToolkitBuilder
from meshagent.tools.storage import StorageToolkitBuilder

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
    def get_toolkit_builders(self):
        return [
            WebSearchToolkitBuilder(),
            StorageToolkitBuilder(),
            LocalShellToolkitBuilder(),
        ]

asyncio.run(service.run())
