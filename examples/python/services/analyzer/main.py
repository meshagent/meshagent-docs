from meshagent.api import RequiredToolkit, RequiredSchema
from meshagent.tools import Toolkit
from meshagent.agents.schemas.document import document_schema
from meshagent.agents.schemas.presentation import presentation_schema
from meshagent.tools.storage import SaveFileFromUrlTool
from meshagent.tools.document_tools import (
    DocumentAuthoringToolkit,
    DocumentTypeAuthoringToolkit,
)
from meshagent.agents.chat import ChatBot
from meshagent.openai import OpenAIResponsesAdapter

import asyncio

from meshagent.api.services import ServiceHost

service = ServiceHost()


@service.path("/agent")
class DocumentAnalyzer(ChatBot):
    def __init__(self):
        super().__init__(
            auto_greet_message="I can create documents and presentations by searching the web or looking at your documents. What would you like me to do?",
            name="meshagent.document.analyzer",
            title="analyzer chatbot",
            description="an chatbot that can analyze documents and write documents or presentations",
            rules=[
                "you are a document authoring assistant which will analyze documents and / or search the web to build content",
                "output document names MUST have the extension .document or .presentation, automatically add the extension if it is not provided",
                "open the document where the output will be written, then examine the contents of the reference file that was provided by the user with markitdown, then use tool calls to write content to the new document",
                "you MUST make at least 1 tool call that writes content into the document before closing it",
                "after opening a document you MUST immediately display it to the user",
                "prefer to add analysis to an output document",
                "you can also search with perplexity to augment information with accurate current sources",
                "for slide backgrounds, you MUST generate a dark abstract background to use as the background using fal, use the subject of the presentation as inspiration for the design",
                "for slides, you MUST generate a background image, save it, and reference its full path as the background",
                "blob URLs MUST not be added to documents, they must be saved as files first",
                "you MUST save images in the .images folder",
                "Unless asked otherwise, presentations should be created with 5 slides.",
                "If asked to insert images or illustrations, you must use flux to create them",
                "each paragraph should be inserted into the document with a seperate tool call",
            ],
            llm_adapter=OpenAIResponsesAdapter(parallel_tool_calls=False),
            requires=[
                RequiredToolkit(name="meshagent.perplexity"),
                RequiredToolkit(
                    name="meshagent.fal", tools=["fal-ai/flux-pro/v1.1-ultra"]
                ),
                RequiredToolkit(
                    name="ui", tools=["ask_user", "display_document", "show_toast"]
                ),
                RequiredToolkit(
                    name="meshagent.markitdown",
                    tools=["markitdown_from_user", "markitdown_from_file"],
                ),
                RequiredSchema(name="document"),
                RequiredSchema(name="presentation"),
            ],
            toolkits=[
                Toolkit(name="local", tools=[SaveFileFromUrlTool()]),
                DocumentAuthoringToolkit(),
                DocumentTypeAuthoringToolkit(
                    schema=document_schema, document_type="document"
                ),
                DocumentTypeAuthoringToolkit(
                    schema=presentation_schema, document_type="presentation"
                ),
            ],
            labels=["chatbot", "documents", "presentations"],
        )


asyncio.run(service.run())
