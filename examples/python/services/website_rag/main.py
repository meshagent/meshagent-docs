from meshagent.api import RequiredToolkit, RequiredSchema
from meshagent.agents.schemas.document import document_schema
from meshagent.tools.document_tools import DocumentAuthoringToolkit, DocumentTypeAuthoringToolkit
from meshagent.agents.hosting import RemoteAgentServer
from meshagent.agents.chat import ChatBot
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.agents.indexer import RagToolkit, SiteIndexer

import asyncio
import os

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

class SampleSiteIndexer(SiteIndexer):
    def __init__(self):
        super().__init__(
            name="meshagent.site_indexer",
            title="site indexer",
            description="indexes a site using firecrawl, pair with a RAG chatbot",
            labels=["tasks", "rag" ])

async def chatbot_server():

    remote_agent_server = RemoteAgentServer(
        cls=RagChatBot,
        path="/webhook",
        validate_webhook_secret=False,
        port=int(os.getenv("MESHAGENT_PORT"))
    )
    await remote_agent_server.run()

async def indexer_server():

    remote_agent_server = RemoteAgentServer(
        cls=SampleSiteIndexer,
        path="/webhook",
        validate_webhook_secret=False,
        port=int(os.getenv("MESHAGENT_PORT")) + 1
    )
    await remote_agent_server.run()

async def server():

    await asyncio.gather(chatbot_server(), indexer_server())

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(server())