# MeshAgent Quickstart: ChatBot

Spin up a text-based chatbot using the MeshAgent CLI. You can run it locally or deploy it as a persistent service in MeshAgent Studio.

## Prerequisites
- MeshAgent account, sign up at [www.meshagent.com](https://www.meshagent.com)
- MeshAgent CLI installed (`uv add "meshagent[all]"`)

## What's included
- `meshagent.yaml` for deploying the agent as a MeshAgent service (uses a public image)

## Tools available to this chatbot
- **Web Search** (`--web-search`): lets the bot look things up on the web.
- **Image Generation** (`--image-generation=gpt-image-1.5`): generate images from prompts.
- **Room Storage** (`--require-storage`): read/write files in the room’s storage (mounted at `/data` when running as a service).
- **MCP** (`--mcp`): enable Model Context Protocol tools (connect external tool providers).

## Option 1: Run Locally
Use this when you want to try the agent without deploying a service. The CLI spins up the agent directly, and it will appear in the room you join for as long as the command is running.

Open your terminal and run:
```bash
meshagent setup
meshagent chatbot join \
  --room=myroom \
  --agent-name=chatbot \
  --image-generation=gpt-image-1.5 \ 
  --mcp \
  --require-storage \
  --web-search 
```
*Note: The --image-generation, --require-storage, --mcp, and --web-search flags are all optional. Only pass flags for the tools you want the agent to have access to*

Now that the agent is running, head to [MeshAgent Studio](https://studio.meshagent.com) to try it out!
1. Open your room (e.g., `myroom`)
2. Under the **Participants** tab select ``chatbot`` and begin working with the agent

## Option 2: Deploy the agent as a service in MeshAgent Studio
Use this when you want the agent to be always available in a room or project. No Dockerfile needed; the YAML points to a maintained public image.

```
meshagent service create --file=meshagent.yaml --room=myroom 
```

- --room is optional. Without it, the service is deployed at the project level and appears in all rooms in your project.
- After it’s live, open the target room in [MeshAgent Studio](https://studio.meshagent.com) and start chatting with `chatbot`.

---
## Learn More 

**Website**: www.meshagent.com(https://www.meshagent.com)
**Documentation**: docs.meshagent.com(https://docs.meshagent.com/)
