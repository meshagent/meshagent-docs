import 'package:meshagent/meshagent.dart';

final schema = MeshSchema(
  rootTagName: 'html',
  elements: [
    ElementType(
      tagName: 'html',
      properties: [
        // A ChildProperty describes the type of children that
        // an element allows. There can be at most one child
        // property for each element type, but the child property
        // can allow multiple types of child elements.
        ChildProperty(
          name: 'children',
          childTagNames: ['body'],
        ),
      ],
    ),
    ElementType(
      tagName: 'body',
      properties: [
        // Our body can only contain paragraph elements.
        ChildProperty(
          name: 'children',
          childTagNames: ['p'],
        ),
      ],
    ),
    ElementType(
      tagName: 'p',
      properties: [
        // A ValueProperty describes an attribute that
        // contains a single value.
        ValueProperty(
          name: 'class',
          type: 'string',
        ),
      ],
    ),
  ],
);

void main() {
  // Here you could do something with `schema`, like
  // passing it to a registry or printing it out.
  print(schema);
}
