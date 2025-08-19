from meshagent.api import RequiredToolkit, RequiredSchema
from meshagent.agents.schemas.document import document_schema
from meshagent.tools.document_tools import (
    DocumentAuthoringToolkit,
    DocumentTypeAuthoringToolkit,
)
from meshagent.agents.hosting import RemoteAgentServer
from meshagent.agents.chat import ChatBot
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.agents.indexer import RagToolkit, StorageIndexer
from meshagent.api.services import ServiceHost

import asyncio
import os

service = ServiceHost()


@service.path("/agent")
class RagChatBot(ChatBot):
    def __init__(self):
        super().__init__(
            name="meshagent.chatbot.storage_rag",
            title="Storage RAG chatbot",
            description="an simple chatbot that does rag, pair with an indexer",
            llm_adapter=OpenAIResponsesAdapter(
                model="gpt-4o-mini", parallel_tool_calls=None
            ),
            rules=[
                "after performing a rag search, do not include citations",
                "output document names MUST have the extension .document, automatically add the extension if it is not provided",
                "after opening a document, display it, before writing to it",
            ],
            requires=[
                RequiredSchema(name="document"),
                RequiredToolkit(
                    name="ui", tools=["ask_user", "display_document", "show_toast"]
                ),
                RequiredToolkit(
                    name="meshagent.markitdown", tools=["markitdown_from_file"]
                ),
            ],
            toolkits=[
                DocumentAuthoringToolkit(),
                DocumentTypeAuthoringToolkit(
                    schema=document_schema, document_type="document"
                ),
                RagToolkit(table="index"),
            ],
            labels=["chatbot", "rag"],
        )


@service.path("/indexer")
class MarkitDownFileIndexer(StorageIndexer):
    def __init__(
        self,
        *,
        name="storage_indexer",
        title="storage indexer",
        description="watch storage and index any uploaded pdfs or office documents",
        labels=["watchers", "rag"],
        chunker=None,
        embedder=None,
        table="index",
    ):
        super().__init__(
            name=name,
            title=title,
            description=description,
            requires=[
                RequiredToolkit(
                    name="meshagent.markitdown", tools=["markitdown_from_file"]
                )
            ],
            labels=labels,
            chunker=chunker,
            embedder=embedder,
            table=table,
        )

    async def read_file(self, *, path: str):
        result = await self.room.agents.invoke_tool(
            toolkit="meshagent.markitdown",
            tool="markitdown_from_file",
            arguments={"path": path},
        )
        return result


async def chatbot_server():
    remote_agent_server = RemoteAgentServer(
        cls=RagChatBot,
        path="/webhook",
        validate_webhook_secret=False,
        port=int(os.getenv("MESHAGENT_PORT")),
    )
    await remote_agent_server.run()


async def indexer_server():
    remote_agent_server = RemoteAgentServer(
        cls=StorageIndexer,
        path="/webhook",
        validate_webhook_secret=False,
        port=int(os.getenv("MESHAGENT_PORT")) + 1,
    )
    await remote_agent_server.run()


asyncio.run(service.run())
