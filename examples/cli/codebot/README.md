# MeshAgent Quickstart: Developer (Codebot)

Spin up a coding focused agent using the MeshAgent CLI. You can run it locally or deploy it as a persistent service in MeshAgent Studio.

## Prerequisites
- MeshAgent account, sign up at [www.meshagent.com](https://www.meshagent.com)
- MeshAgent CLI installed (`uv add "meshagent[all]"`)

## What's included
- `meshagent.yaml` for deploying the agent as a MeshAgent service (uses a public image)

## Tools available in this agent
- **Local Shell** (`--require-local-shell`): run commands in a sandboxed shell.
- **Web Search** (`--web-search`): look up information on the web.
- **MCP** (`--mcp`): enable Model Context Protocol tools (connect external tool providers).

## Option 1: Run Locally
Use this when you want to try the agent without deploying a service. The CLI spins up the agent directly, and it will appear in the room you join for as long as the command is running.

Open your terminal and run:
```bash
meshagent setup
meshagent chatbot join \
  --room=myroom \
  --agent-name=developer \
  --require-local-shell \
  --mcp \
  --web-search \
  --rule='You are an agent to assist users with a command line. The root of the filesystem that the user sees has been mounted in the /data folder. You can only write to the /data folder, the rest of your file system is read only.'
```

Now that the agent is running, head to [MeshAgent Studio](https://studio.meshagent.com) to try it out!
1. Open your room (e.g., `myroom`)
2. Under the **Participants** tab select `developer` and begin working with the agent

## Option 2: Deploy the agent as a service in MeshAgent Studio
Use this when you want the agent to be always available in a room or project. No Dockerfile needed; the YAML points to a maintained public image.

```
meshagent service create --file=meshagent.yaml --room=myroom 
```

- --room is optional. Without it, the service is deployed at the project level and appears in all rooms in your project.
- After it’s live, open the target room in [MeshAgent Studio](https://studio.meshagent.com) and start chatting with `developer`.

---
## Learn More 

**Website**: www.meshagent.com(https://www.meshagent.com)
**Documentation**: docs.meshagent.com(https://docs.meshagent.com/)
