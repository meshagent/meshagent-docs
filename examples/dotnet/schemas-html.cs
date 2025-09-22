using Meshagent.Api.Schema;
using System.Collections.Generic;

var schema = new MeshSchema(
    rootTagName: "html",
    elements: new List<ElementType>
    {
        new ElementType(
            tagName: "html",
            properties: new List<ElementProperty>
            {
                // A ChildProperty describes the type of children an element allows
                new ChildProperty(
                    name: "children",
                    childTagNames: new List<string> { "body" }
                )
            }
        ),
        new ElementType(
            tagName: "body",
            properties: new List<ElementProperty>
            {
                // Our body can only contain paragraph elements
                new ChildProperty(
                    name: "children",
                    childTagNames: new List<string> { "p" }
                )
            }
        ),
        new ElementType(
            tagName: "p",
            properties: new List<ElementProperty>
            {
                // A ValueProperty describes an attribute that contains a single value
                new ValueProperty(
                    name: "class",
                    type: SimpleValue.String
                )
            }
        )
    }
);