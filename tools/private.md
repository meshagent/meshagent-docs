---
order: -3
---

# Dynamic User Interfaces

Dynamic User Interfaces enable agents to interact directly with users by presenting responsive, on-demand interfaces. With the ability to execute tools remotely, **MeshAgent** empowers agents to invoke and leverage user interface tools as needed.

## Private Tool Registrations

Consider a collaborative environment where multiple users work alongside a group of agents. In such scenarios, agents may occasionally need to engage individual users—for example, to display notifications, request files, or gather specific information. To facilitate these interactions, the application can register specialized tools that agents can call upon.

**How does an agent target a specific user with a dialog?**  
MeshAgent addresses this by supporting *private tool registrations*. When a user interface registers a private tool, that tool is accessible only to the registering user. An agent can then invoke this private tool by including the unique identifier of the user (the participant ID) in its call. This ensures that the interface is displayed solely to the intended recipient.

For instance, let’s update our Adder agent sample: instead of the studio collecting parameters externally, the agent now directly prompts the user for input by invoking the relevant private tool.

---
+++ Python
:::code source="/examples/python/private-tool-call.py":::
+++

Run the agent, connect to the "examples" room, and then invoke the agent from the Tasks menu in the studio. The agent will gather the inputs from the user and then return the result.

## Intergrating with Your Own Applications 

The studio registers a set of user interface tools which you can use right away. To enable your agents to work either inside the Meshagent Studio or inside your own applications, your user interface can register a toolkit with the same name, and tools with the same name and schema as the ones available inside the studio. Then, when a participant from your own application invokes the tool, it will display your application's custom interface but it will continue to be usable directly from the studio. The key thing to remember is that the application needs to use a private tool registration so that it does not conflict with the studio.