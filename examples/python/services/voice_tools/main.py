from meshagent.livekit.agents.voice import VoiceBot
from meshagent.api.services import ServiceHost
from meshagent.api import RequiredToolkit, RequiredSchema
from meshagent.tools import Toolkit
import asyncio
from meshagent.tools.document_tools import (
    DocumentAuthoringToolkit,
    DocumentTypeAuthoringToolkit,
)
from meshagent.server.outputs.document import document_schema
from meshagent.tools.storage import SaveFileFromUrlTool
from meshagent.markitdown.tools import MarkItDownToolkit

import livekit.agents.utils.http_context
import livekit.agents.cli.log

service = ServiceHost()

context = livekit.agents.utils.http_context._new_session_ctx()
livekit.agents.cli.log.setup_logging("ERROR", True, True)


@service.path("/agent")
class SampleVoiceAgentWithTools(VoiceBot):
    def __init__(self):
        super().__init__(
            name="meshagent.livekit.agent_with_tools",
            title="voice agent with tools",
            description="sample agent that will respond to a query via voice",
            labels=["voice"],
            auto_greet_prompt="hello",
            rules=[
                "You are a helpful assistant communicating through voice.",
                "When editing an element, do not also insert the element into the root, only change the attributes of the element",
                "output document names MUST have the extension .document automatically add the extension if it is not provided",
                "when writing a document, open the document where the output will be written, then examine the contents of the reference file that was provided by the user with markitdown, then use tool calls to write content to the new document",
                "you MUST make at least 1 tool call that writes content into the document before closing it",
                "after opening a document you MUST immediately display it to the user",
                "prefer to add analysis to an output document",
                "each paragraph MUST be inserted into the document with a seperate tool call",
                "you MUST only include a single paragraph per tool call when inserting content",
                "if you close a document, it needs to be opened before you can update attributes or insert elements in it",
                "if you need to ask the user something, you should use the say tool before invoking the ask_user tool to let the user know why they are being asked something.",
            ],
            requires=[
                RequiredToolkit(
                    name="ui", tools=["ask_user", "display_document", "show_toast"]
                ),
            ],
            toolkits=[
                MarkItDownToolkit(),
                Toolkit(name="local", tools=[SaveFileFromUrlTool()]),
                DocumentAuthoringToolkit(),
                DocumentTypeAuthoringToolkit(
                    schema=document_schema, document_type="document"
                ),
            ],
        )


@service.path("/interviewer")
class SampleVoiceAgentWithTools(VoiceBot):
    def __init__(self):
        super().__init__(
            name="meshagent.livekit.agent_with_tools",
            title="voice agent with tools",
            description="sample agent that will respond to a query via voice",
            labels=["voice"],
            auto_greet_prompt="hello",
            rules=[
                "You are a helpful assistant communicating through voice.",
                "When editing an element, do not also insert the element into the root, only change the attributes of the element",
                "output document names MUST have the extension .document automatically add the extension if it is not provided",
                "when writing a document, open the document where the output will be written, then examine the contents of the reference file that was provided by the user with markitdown, then use tool calls to write content to the new document",
                "you MUST make at least 1 tool call that writes content into the document before closing it",
                "after opening a document you MUST immediately display it to the user",
                "prefer to add analysis to an output document",
                "each paragraph MUST be inserted into the document with a seperate tool call",
                "you MUST only include a single paragraph per tool call when inserting content",
                "if you close a document, it needs to be opened before you can update attributes or insert elements in it",
                "if the user asks you to interview them, keep a document open while you are interviewing them and write the questions and answers to the document as you go",
            ],
            requires=[
                RequiredToolkit(name="ui", tools=["display_document", "show_toast"]),
            ],
            toolkits=[
                MarkItDownToolkit(),
                Toolkit(name="local", tools=[SaveFileFromUrlTool()]),
                DocumentAuthoringToolkit(),
                DocumentTypeAuthoringToolkit(
                    schema=document_schema, document_type="document"
                ),
            ],
        )


asyncio.run(service.run())
