from meshagent.api.schema import MeshSchema, ElementType, ChildProperty, ValueProperty

schema = MeshSchema(
    root_tag_name="html",
    elements=[
        ElementType(
            tag_name="html",
            properties=[
                # a ChildProperty describes the type of children that an element allows. There can at most one child
                # property for each element type, but the child property can allow multiple types of child elements
                ChildProperty(name="children", child_tag_names=["body"])
            ]),
        
        ElementType(
            tag_name="body",
            properties=[
                # Our body can only contain paragraph elements
                ChildProperty(name="children", child_tag_names=["p"])
            ]),
        
        ElementType(
            tag_name="p",
            properties=[
                # A ValueProperty property describes an attribute that contains a single value
                ValueProperty(name="class", type="string"),
            ]),
    ]
)