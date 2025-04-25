from meshagent.api import RequiredToolkit, RequiredSchema
from meshagent.tools import Toolkit
from meshagent.agents.schemas.gallery import gallery_schema
from meshagent.tools.storage import SaveFileFromUrlTool
from meshagent.tools.document_tools import DocumentAuthoringToolkit, DocumentTypeAuthoringToolkit
from meshagent.agents.hosting import RemoteAgentServer
from meshagent.agents.chat import ChatBot
from meshagent.openai import OpenAIResponsesAdapter



import asyncio
import os

class Designer(ChatBot):
    def __init__(self):
        super().__init__(
            name="meshagent.designer.images",
            title="image designer",
            description="an agent that generates images and videos",
            empty_state_title="What images can I make for you?",
            rules=[
                "you should always use sync mode for fal tools, num images should always be one when calling fal (use multiple calls if multiple images are requested)",
                "you are an assistant for generating images using flex pro ultra",
                "if asked by the user to generate images, use the ask_user tool to ask the user what kinds of images they would like you to create",
                "if asked by the user to generate images, use flux pro ultra to generate the images, save all of the images",
                "before generating the images, open a document that will be used to display the images, and check for any existing content in the document",
                "use the flux defaults, but allow the user to select a different aspect ratio",
                "after each image is generated, you MUST insert it into the document so that the user can see the image",
                "after generating an image you MUST insert it into the document before generating another image",
                "images should be saved to the .images folder"
                "when inserting files, you MUST use the full path to the file",
                "the document names MUST have the extension .gallery, automatically add the extension if it is not provided",
                "you MUST always add generated images to a document",
                "get_file_download_url MUST NOT be passed a blob url, it can only be passed file paths",
                "if asked to upscale an image, use image to image, or for a tool that requires an image_url as input, use the get_file_download_url with the the complete file path of the image that was added to the document to get the image_url",
                "leave the document open, it will automatically close on termination",
                "blob URLs MUST not be added to galleries, they must be saved first",
                "after opening a document, immediately display it to the user",
            ],
            llm_adapter = OpenAIResponsesAdapter(parallel_tool_calls=True),
            requires = [
                RequiredToolkit(name="meshagent.fal", tools=[
                        "fal-ai/flux-pro/v1.1-ultra",
                        "fal-ai/flux/dev/image-to-image",
                        "fal-ai/veo2",
                        "fal-ai/veo2/image-to-video"
                    ]
                ),
                RequiredToolkit(name="ui",
                    tools=[
                        "ask_user",
                        "display_document",
                        "show_toast"
                    ]
                ),
                RequiredSchema(name="gallery"),
                RequiredToolkit(name="meshagent.markitdown", tools=[ "markitdown_from_user", "markitdown_from_file" ]),
            ],
            toolkits=[
                Toolkit(name="local", tools=[
                    SaveFileFromUrlTool()
                ]),
                DocumentAuthoringToolkit(),
                DocumentTypeAuthoringToolkit(
                    schema=gallery_schema,
                    document_type="gallery"
                )
                
            ],
            auto_greet_message="What images can I help you design?",
            labels=[ "tasks", "images" ]
        )


async def server():

    remote_agent_server = RemoteAgentServer(
        cls=Designer,
        path="/webhook",
        validate_webhook_secret=False,
        port=int(os.getenv("MESHAGENT_PORT"))
    )
    await remote_agent_server.run()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(server())