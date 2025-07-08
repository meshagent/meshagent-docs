from meshagent.api import RequiredSchema
from meshagent.agents.schemas.document import document_schema
from meshagent.tools.document_tools import DocumentAuthoringToolkit, DocumentTypeAuthoringToolkit
from meshagent.agents.planning import PlanningResponder
from meshagent.openai import OpenAIResponsesAdapter

import asyncio

from meshagent.api.services import ServiceHost

service = ServiceHost()
@service.path("/agent")
class DocumentAuthor(PlanningResponder):
    def __init__(self):

        super().__init__(
            name="meshagent.document-author",
            title="document task",
            output_schema={
                "type" : "object",
                "required" : [],
                "additionalProperties" : False,
                "properties" : {
                }
            },
            description="an task runner that author documents and use tools",
            rules=[
                "you are a document authoring assistant",
                "the user will provide a prompt that is suitable for creating a document",
                "you MUST generate at least one document as a result of the user's query",
                "use the ask_user tool to pick the name of a document, pick a document name if the tool is not available.",
                "the document names MUST have the extension .document, automatically add the extension if it is not provided",
                "you MUST always write content to a document",
                "first open a document, then use tools to write the document content before closing the document",
                "before closing the document, ask the user if they would like any additional modifications to be made to the document, and if so, make them. continue to ask the user until they are happy with the contents. you are not finished until the user is happy.",
                "blob URLs MUST not be added to documents, they must be saved as files first",
            ],
            llm_adapter = OpenAIResponsesAdapter(
                parallel_tool_calls=False
            ),
            supports_tools = True,
            requires=[
                RequiredSchema(
                    name="document"
                )
            ],
            toolkits=[
                DocumentAuthoringToolkit(),
                DocumentTypeAuthoringToolkit(
                    schema=document_schema,
                    document_type="document"
                )
            ],
            labels=[ "tasks", "documents" ]
        )

asyncio.run(service.run())