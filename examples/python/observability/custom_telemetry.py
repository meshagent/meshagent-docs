import asyncio
import logging
import time

from meshagent.otel import otel_config
from meshagent.api.services import ServiceHost
from meshagent.agents.chat import ChatBot, ChatThreadContext
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.api import RemoteParticipant, MeshDocument

from opentelemetry import trace, metrics


otel_config(service_name="instrumented-chatbot")

tracer = trace.get_tracer("examples.custom_telemetry")
meter = metrics.get_meter("examples.custom_telemetry")
response_counter = meter.create_counter(
    "chatbot.responses", unit="1", description="Assistant messages sent"
)
context_histogram = meter.create_histogram(
    "chatbot.context.prepare_ms",
    unit="ms",
    description="Latency while preparing the chat context",
)

logger = logging.getLogger("examples.custom_telemetry")

service = ServiceHost()


def _latest_user_message(context: ChatThreadContext) -> str | None:
    for message in reversed(context.chat.messages):
        if message.get("role") == "user" and isinstance(message.get("content"), str):
            return message["content"]
    return None


@service.path(path="/chat", identity="chatbot")
class InstrumentedChatbot(ChatBot):
    def __init__(self):
        super().__init__(
            name="chatbot",
            title="Instrumented Chatbot",
            description="Adds custom traces, logs, and metrics",
            rules=[
                "Always greet the user and include a friendly fun fact at the end of the reply."
            ],
            llm_adapter=OpenAIResponsesAdapter(),
        )

    async def prepare_llm_context(self, *, thread_context: ChatThreadContext):
        start = time.perf_counter()
        with tracer.start_as_current_span("chatbot.prepare_context") as span:
            message_count = len(thread_context.chat.messages)
            span.set_attribute("meshagent.chat.messages", message_count)
            span.set_attribute("meshagent.thread.path", thread_context.path)

            last_user_message = _latest_user_message(thread_context)
            if last_user_message:
                span.add_event(
                    "user_message.preview",
                    {"preview": last_user_message[:120]},
                )

            logger.info(
                "preparing context",
                extra={
                    "path": thread_context.path,
                    "message_count": message_count,
                },
            )

            await super().prepare_llm_context(thread_context=thread_context)

        elapsed_ms = (time.perf_counter() - start) * 1000
        context_histogram.record(
            elapsed_ms,
            attributes={"meshagent.thread.path": thread_context.path},
        )

    async def _send_and_save_chat(
        self,
        thread: MeshDocument,
        path: str,
        to: RemoteParticipant,
        id: str,
        text: str,
        thread_attributes: dict,
    ):
        with tracer.start_as_current_span("chatbot.send_response") as span:
            span.set_attribute("meshagent.thread.path", path)
            span.set_attribute("meshagent.response.id", id)
            span.set_attribute("meshagent.recipient.id", to.id)
            span.set_attribute("meshagent.response.length", len(text))

            span.add_event(
                "response.preview",
                {"preview": text[:120]},
            )

            logger.info(
                "sending response",
                extra={
                    "path": path,
                    "response_id": id,
                    "characters": len(text),
                },
            )

            response_counter.add(
                1,
                attributes={
                    "meshagent.thread.path": path,
                    "meshagent.recipient.id": to.id,
                },
            )

        return await super()._send_and_save_chat(
            thread=thread,
            path=path,
            to=to,
            id=id,
            text=text,
            thread_attributes=thread_attributes,
        )


asyncio.run(service.run())
