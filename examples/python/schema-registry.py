from meshagent.api import SchemaRegistry, SchemaRegistration, MeshSchema, ElementType, ChildProperty, ValueProperty
import asyncio


sample = MeshSchema(
    root_tag_name="sample",
    elements=[
        ElementType(
            description="test",
            tag_name="sample",
            properties=[
                ChildProperty(name="children", description="desc", child_tag_names=[
                    "child"
                ]),
        ]),
        ElementType(tag_name="child", description="child", properties=[
            ValueProperty(name="prop", description="desc", type="number")
        ]),
    ]
)

async def main():    
    server = SchemaRegistry(schemas=[
        SchemaRegistration(name="sample", schema=sample)
    ])
    await server.run()

asyncio.run(main())
