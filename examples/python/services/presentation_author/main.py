from meshagent.api import RequiredSchema, RequiredToolkit
from meshagent.agents.schemas.presentation import presentation_schema
from meshagent.tools.storage import SaveFileFromUrlTool
from meshagent.tools import Toolkit
from meshagent.tools.document_tools import (
    DocumentAuthoringToolkit,
    DocumentTypeAuthoringToolkit,
)
from meshagent.agents.planning import PlanningResponder
from meshagent.openai import OpenAIResponsesAdapter
from meshagent.api.services import ServiceHost

import asyncio

service = ServiceHost()


@service.path("/agent")
class PresentationAuthor(PlanningResponder):
    def __init__(self):
        super().__init__(
            name="meshagent.presentation-author",
            title="presentation task",
            output_schema={
                "type": "object",
                "required": [],
                "additionalProperties": False,
                "properties": {},
            },
            description="an task runner that author presentations and use tools",
            rules=[
                "you are a presentation authoring assistant",
                "the user will provide a prompt that is suitable for creating a presentation",
                "you MUST generate at least one presentation as a result of the user's query",
                "use the ask_user tool to pick the name of a presentation, pick a presentation name if the tool is not available.",
                "the presentation names MUST have the extension .presentation, automatically add the extension if it is not provided",
                "you MUST always write content to a presentation",
                "first open a presentation, then use tools to write the document content",
                "leave the document open, it will be closed automatically",
                "for slide backgrounds, you MUST generate a dark abstract background to use as the background",
                "for slides, you MUST generate a background image, save it, and reference its full path as the background",
                "blob URLs MUST not be added to documents, they must be saved as files first",
                "you MUST save images in the .images folder",
            ],
            llm_adapter=OpenAIResponsesAdapter(parallel_tool_calls=False),
            supports_tools=True,
            requires=[
                RequiredToolkit(
                    name="meshagent.fal",
                    tools=[
                        "fal-ai/flux-pro/v1.1-ultra",
                    ],
                ),
            ],
            toolkits=[
                DocumentAuthoringToolkit(),
                DocumentTypeAuthoringToolkit(
                    schema=presentation_schema, document_type="presentation"
                ),
                Toolkit(name="local", tools=[SaveFileFromUrlTool()]),
            ],
            labels=["tasks", "presentations"],
        )


asyncio.run(service.run())
