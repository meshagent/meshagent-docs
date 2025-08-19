import {
  SchemaRegistry,
  SchemaRegistration,
  MeshSchema,
  ElementType,
  ChildProperty,
  ValueProperty,
} from '@meshagent/meshagent';

// Define the schema
const sample = new MeshSchema({
  rootTagName: 'sample',
  elements: [
    new ElementType({
      tagName: 'sample',
      description: 'test',
      properties: [
        new ChildProperty({
          name: 'children',
          description: 'desc',
          childTagNames: ['child'],
        }),
      ],
    }),
    new ElementType({
      tagName: 'child',
      description: 'child',
      properties: [
        new ValueProperty({
          name: 'prop',
          description: 'desc',
          type: 'number',
        }),
      ],
    }),
  ],
});

// Main async function to run the server
async function main(): Promise<void> {
  const server = new SchemaRegistry({
    schemas: [
      new SchemaRegistration({
        name: 'sample',
        schema: sample,
      }),
    ],
  });

  // Start the server
  await server.run();
}

// Entry point
try {
  main();
} catch (error) {
  console.error('Error:', error);
}
