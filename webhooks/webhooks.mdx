# Webhooks

## What Are Webhooks?

**Webhooks** are HTTP callbacks that send real-time notifications when a specific event occurs. Instead of your service constantly polling MeshAgent for updates, MeshAgent delivers event data to your configured webhook endpoint. This is especially useful for triggering workflows or data processing in response to events such as:

- A new room starting
- A room ending
- Other significant lifecycle events in MeshAgent

By leveraging webhooks, you can extend or integrate MeshAgent functionality into external systems—like logging, dashboards, or automated tasks (e.g., automatically registering an agent when a room starts).

---

## Setting Up a Webhook

To add a webhook in MeshAgent:

1. **Navigate to your project settings.**
2. **Enter the URL** of the server or service that should receive event notifications.

When events occur, MeshAgent will send an HTTP request with relevant event data (for example, when a room starts or ends). 

---

## Built-in Webhook Server

While you can receive events on any web server, MeshAgent provides a **built-in webhook server** to simplify things. You can enable and extend this server by subclassing it. 

### Environment Variable

The built-in server expects the secret to be provided through the `MESHAGENT_WEBHOOK_SECRET` environment variable. MeshAgent will use this secret to verify that incoming webhook requests are valid.

### Default Port

By default, the webhook server listens on **port 8080** and exposes two routes:

1. `"/"` — Returns an HTTP 200 response for any request. (Useful for health checks in hosting environments like Cloud Run.)
2. `"/webhook"` — The main endpoint that verifies incoming requests using the secret and then processes valid webhook payloads.

---

## Example: Creating a Custom Webhook Server

The following code shows how to create and run a basic custom webhook server. This server listens for **room started** and **room ended** events and then prints them.

+++ Python
:::code source="/examples/python/webhooks.py":::
+++

---

## Verifying Webhook Signatures

By providing the `MESHAGENT_WEBHOOK_SECRET` in your environment, MeshAgent signs each webhook request. This allows the built-in server (and your custom logic) to verify the authenticity of incoming requests—helping protect you from malicious or unintended calls.


**Why you might want this**: 
- Automatically send notifications to external monitoring tools when rooms start or end.
- Kick off background tasks (e.g., data collection or analytics) at the start or end of a room session.
- Register agents or tools with a room automatically

---

## Example: Auto-Register an Agent on Room Start

A common scenario is to **automatically register an agent** with new rooms as they start. MeshAgent provides a built-in class that can handle this for you. Below is an example of how to create an agent (in this case, a simple “adder” agent) and have it automatically register in every new room. In 

+++ Python
:::code source="/examples/python/agent-server.py":::
+++

---

## Environment Variables

In addition to the `MESHAGENT_WEBHOOK_SECRET` variable, the server will look for the standard environment variables for meshagent API keys and project settings. You can find these values in the settings of your project by viewing an existing API key or creating a new one.

**Why you might want this**:
- Ensure a specific agent is always available in new rooms, providing real-time functionality (such as an auto-moderator, a data aggregator, or a Q&A assistant).
- Centralize and automate agent deployment rather than manually adding the agent to each new room.


---

## Next Steps

- **Customize event handling**: Override methods to handle more event types as your application grows.
- **Deploy your server**: Run your webhook server on platforms like Docker, AWS, or Google Cloud.
- **Manage secrets securely**: Store `MESHAGENT_WEBHOOK_SECRET` in a secure storage solution (e.g., AWS Secrets Manager, GCP Secret Manager, or environment variables in a locked-down environment).

For more advanced use cases, combine your webhook server with MeshAgent’s API to dynamically respond to events by creating or modifying rooms, registering different agents, or integrating with external services. 

---

## Summary

Webhooks are a powerful way to integrate MeshAgent events with external systems. Whether you want to log room activities, trigger custom automations, or automatically register agents, the MeshAgent webhook system—along with its built-in server—makes these integrations straightforward and secure.