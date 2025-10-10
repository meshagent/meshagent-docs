from meshagent.api import RequiredToolkit, RequiredSchema
from meshagent.agents.schemas.document import document_schema
from meshagent.tools.document_tools import (
    DocumentAuthoringToolkit,
    DocumentTypeAuthoringToolkit,
)
from meshagent.agents.chat import ChatBot
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.agents.indexer import (
    RagToolkit,
    StorageIndexer,
    Embedder,
    OpenAIEmbedder,
)
from meshagent.agents.agent import SingleRoomAgent
from meshagent.api.services import ServiceHost
from meshagent.markitdown.tools import MarkItDownToolkit
from meshagent.tools import ToolContext
from meshagent.openai.proxy import get_client

import asyncio
from contextlib import suppress

service = ServiceHost()


@service.path(path="/agent", identity="meshagent.chatbot.storage_rag")
class RagChatBot(ChatBot):
    def __init__(self):
        self._rag_embedder = _DeferredEmbedder()
        self._rag_toolkit = RagToolkit(table="rag-index", embedder=self._rag_embedder)

        super().__init__(
            name="meshagent.chatbot.storage_rag",
            title="Storage RAG chatbot",
            description="an simple chatbot that does rag, pair with an indexer",
            llm_adapter=OpenAIResponsesAdapter(),
            rules=[
                "after performing a rag search, do not include citations",
                "output document names MUST have the extension .document, automatically add the extension if it is not provided",
                "after opening a document, display it, before writing to it",
            ],
            requires=[
                RequiredSchema(name="document"),
                RequiredToolkit(
                    name="ui", tools=["ask_user", "display_document", "show_toast"]
                )
            ],
            toolkits=[
                MarkItDownToolkit(),
                DocumentAuthoringToolkit(),
                DocumentTypeAuthoringToolkit(
                    schema=document_schema, document_type="document"
                ),
                self._rag_toolkit,
            ],
            labels=["chatbot", "rag"],
        )

    async def start(self, *, room):
        self._rag_toolkit.tools[0]._embedder = OpenAIEmbedder(
            size=3072,
            max_length=8191,
            model="text-embedding-3-large",
            openai=get_client(room=room),
        )
        await super().start(room=room)

class _DeferredEmbedder(Embedder):
    def __init__(self):
        super().__init__(size=0, max_length=0)

    async def embed(self, *, text: str) -> list[float]:
        raise RuntimeError("Embedder not initialized yet")

@service.path(path="/indexer", identity="storage_indexer")
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
        table="rag-index",
    ):
        self._markitdown = MarkItDownToolkit()
        if embedder is None:
            embedder = _DeferredEmbedder()
        super().__init__(
            name=name,
            title=title,
            description=description,
            labels=labels,
            chunker=chunker,
            embedder=embedder,
            table=table,
        )

    async def read_file(self, *, path: str):
        context = ToolContext(
            room=self.room,
            caller=self.room.local_participant,
        )
        response = await self._markitdown.execute(
            context=context,
            name="markitdown_from_file",
            arguments={"path": path},
        )
        return getattr(response, "text", None)

    async def start(self, *, room):
        self.embedder = OpenAIEmbedder(
            size=3072,
            max_length=8191,
            model="text-embedding-3-large",
            openai=get_client(room=room),
        )
        await super().start(room=room)

    async def stop(self):
        if getattr(self, "_chan", None) is not None and not self._chan.closed:
            self._chan.close()

        index_task = getattr(self, "_index_task", None)
        if index_task is not None and not index_task.done():
            index_task.cancel()
            with suppress(Exception):
                await index_task

        await SingleRoomAgent.stop(self)

asyncio.run(service.run())
