---
order: -1
---

# Documents

MeshDocuments enable your agents to share and synchronize information in real time across platforms. They resemble a web page’s structure but offer much greater flexibility. For example, if you want to generate website content with your agents, you can start with a simple HTML-compatible document format:

```html
<html>
    <body>
        <p class="content"></p>
    </body>
</html>

```

A MeshDocument, like an HTML document, is composed of elements that can have child elements and attributes. However, MeshDocuments introduce additional features and capabilities that go beyond standard HTML or XML.

## Defining Your Document Structure

To define the structure of a MeshDocument, you start by creating a schema using the MeshSchema class. A schema:

- Documents the structure of your MeshDocument for anyone in your organization.
- Ensures agents and users don’t write invalid data to the document.
- Allows agents to automatically generate, manipulate, and validate structured documents.
- Automatically generates LLM-compatible schemas for structured outputs.
- Synchronizes documents across all platforms that MeshAgent supports.

Similar to how a web page is structured, a MeshSchema begins with a root element that includes an allowed tag name and optional attributes. Afterward, you can define additional tags, their attributes, and the types of child nodes they can contain.

### Example Schema

Suppose you have a basic web page structure and want to define a schema for it. In Python:

+++ Python
:::code source="/examples/python/schemas-html.py" :::
+++

# Creating a MeshDocument

Many LLMs (such as OpenAI) and agent frameworks (such as MeshAgent) support JSON Schemas for defining inputs and outputs. Generating an OpenAI-compatible JSON schema from your MeshSchema requires only one line of code:

+++ Python
:::code source="/examples/python/schemas-json.py" :::
+++

To create a MeshDocument based on your schema and enable synchronization across different clients, use the MeshAgent runtime:

+++ Python
:::code source="/examples/python/documents-writing.py" :::
+++

Once you have a MeshDocument, you can [build an agent](/quickstart/agents/) that knows how to write to it.