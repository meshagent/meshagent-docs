from meshagent.api import RequiredToolkit, RequiredSchema
from meshagent.agents.schemas.document import document_schema
from meshagent.tools.document_tools import DocumentAuthoringToolkit, DocumentTypeAuthoringToolkit
from meshagent.agents.chat import ChatBot
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.agents.indexer import RagToolkit, SiteIndexer
from meshagent.api.services import ServiceHost

import asyncio
import os

service = ServiceHost()


@service.path("/agent")
class RagChatBot(ChatBot):
    def __init__(self):
        super().__init__(
            name="meshagent.chatbot.website_rag",
            title="Website RAG chatbot",
            description="an simple chatbot that does rag, pair with an indexer",
            llm_adapter = OpenAIResponsesAdapter(
                model="gpt-4o-mini",
                parallel_tool_calls=None
            ),
            rules=[
                "after performing a rag search, do not include citations",
                "output document names MUST have the extension .document, automatically add the extension if it is not provided",
                "after opening a document, display it, before writing to it"
            ],
            requires=[
                RequiredSchema(
                    name="document"
                ),
                RequiredToolkit(
                    name="ui",
                    tools=[
                        "ask_user",
                        "display_document",
                        "show_toast"
                    ]
                ),
                RequiredToolkit(
                    name="meshagent.markitdown",
                    tools=[ "markitdown_from_file" ]
                )
            ],
            toolkits=[
                DocumentAuthoringToolkit(),
                DocumentTypeAuthoringToolkit(
                    schema=document_schema,
                    document_type="document"
                ),
                RagToolkit(table="index"),
            ],
            labels=[ "chatbot", "rag" ]
        )

@service.path("/indexer")
class SampleSiteIndexer(SiteIndexer):
    def __init__(self):
        super().__init__(
            name="meshagent.site_indexer",
            title="site indexer",
            description="indexes a site using firecrawl, pair with a RAG chatbot",
            labels=["tasks", "rag" ])

asyncio.run(service.run())