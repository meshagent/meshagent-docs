# Deploying a MeshAgent Schema

MeshAgent uses _schemas_ to define how data can be structured and synchronized across rooms using MeshDocuments. By deploying a schema, you make it available to any room that needs it for data exchange. Below is a guide on how you can:

1. Manually add a schema to a room if you already know the room names in advance, or  
2. Automatically deploy a schema to newly created rooms by listening for a “room created” webhook.

---

##  Manual Registration

If you know your room names up front, you can simply add the schema to each room directly. This is the simplest approach when the room names are predetermined:

```python
from meshagent.api import deploy_schema, RoomClient, websocket_protocol

# When you want to deploy a schema manually, you can connect to the room and use the deploy_schema function.

    async with RoomClient(protocol = websocket_protocol(participant_name="schema_registrar", room_name="my_room", role="agent")) as room:

        # This will place the schema in the room under .schemas/sample.json and make it available for use in documents with the .sample extension
        await deploy_schema(room=room, schema=mesh_schema, name="sample")

```

Replace `my_room` with your actual room name(s). By doing this for each known room, your custom schema is immediately available for use by any MeshDocuments within those rooms.

---

## Automatic Deployment for Dynamic Rooms

When room names are dynamic, it’s easier to automatically register or update your schema whenever a new room is created. You can achieve this by:

1. **Listening for a “room created” webhook**. MeshAgent can notify your service whenever a new room is spun up.  
2. **Registering the schema upon room creation**. In the webhook handler, you can deploy the schema to the new room.

### Flow

1. **Subscribe to the "room created" event** in your application or service.  
2. **Use `SchemaRegistry`** to write your custom schema to the newly created room, ensuring it is ready for use by MeshDocuments.  

---

## Sample Code

Here is a minimal example demonstrating how to define and run a custom schema registry with MeshAgent. 

+++ Python
:::code source="/examples/python/schema-registry.py":::
+++

---

## Conclusion

Deploying a custom MeshAgent schema is a straightforward process. Whether you add it manually to known rooms or use webhooks to deploy it automatically to newly created ones, the core idea is to define your `MeshSchema` and register it with `SchemaRegistry`. This allows any MeshDocument in that room to immediately leverage the schema for structured data synchronization.