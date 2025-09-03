from meshagent.tools import Tool, RemoteToolkit, Toolkit
from meshagent.api.services import ServiceHost
from meshagent.agents.chat import ChatBot
from meshagent.api import MeshDocument
from meshagent.openai.tools import OpenAIResponsesAdapter
import json

import asyncio

service = ServiceHost()


class ProductWidget(Tool):
    def __init__(self):
        super().__init__(
            name="products",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "data",
                    "platform",
                    "output",
                ],
                "properties": {
                    "data": {"type": "string"},
                    "platform": {"type": "string"},
                    "output": {"type": "string"},
                },
            },
        )

    async def execute(self, context, *, platform: str, data: str, output: str):
        return """
import core;
import core.widgets;
import material;

widget root = Container(
    height: 200,
    width: 400,
    child: ListView(
        scrollDirection: "horizontal",
        children: [
        ...for product in data.data.products:
            Product(product: product)
        ],
    )
);

widget Product = Container(width: 200, height: 200, 
decoration: {
      type: "shape",
      shape: {
        type: "stadium",
        side: { width:1.0 },
      },
      gradient: {
        type: "linear",
        begin: { x: -0.5, y: -0.25 },
        end: { x: 0.0, y: 0.5 },
        colors: [ 0xFFFFFF99, 0xFFEEDD00 ],
        stops: [ 0.0, 1.0 ],
        tileMode: "mirror",
      },
    },
      child: 
 Center(   child: Text(text: args.product.name, style: { color: 0xff000000 })),
);

"""


@service.path("/renderer", identity="renderer")
class DynamicUI(RemoteToolkit):
    def __init__(self):
        super().__init__(name="renderer", tools=[ProductWidget()])


class InsertProductListingTool(Tool):
    def __init__(self, thread: MeshDocument):
        self.thread = thread
        super().__init__(
            name="insert_product_listing",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["products"],
                "properties": {
                    "products": {
                        "type": "array",
                        "items": {
                            "anyOf": [
                                {
                                    "type": "object",
                                    "required": ["name"],
                                    "additionalProperties": False,
                                    "properties": {"name": {"type": "string"}},
                                }
                            ]
                        },
                    }
                },
            },
        )

    async def execute(self, context, products: list):
        for child in self.thread.root.get_children():
            if child.tag_name == "messages":
                child.append_child(
                    "ui",
                    {
                        "renderer": "renderer",
                        "widget": "products",
                        "data": json.dumps({"products": products}),
                    },
                )


class ProductToolkit(Toolkit):
    def __init__(self, thread: MeshDocument):
        super().__init__(name="products", tools=[InsertProductListingTool(thread)])


@service.path("/chatbot", identity="product-chatbot")
class UIChatBot(ChatBot):
    def __init__(self):
        super().__init__(
            name="chatbot",
            llm_adapter=OpenAIResponsesAdapter(),
            rules=[
                "use the insert_product_listing tool to display a list of products when asked about products"
            ],
        )

    async def get_thread_toolkits(self, *, thread_context, participant):
        toolkits = await super().get_thread_toolkits(
            thread_context=thread_context, participant=participant
        )
        toolkits.append(ProductToolkit(thread=thread_context.thread))
        return toolkits


asyncio.run(service.run())
