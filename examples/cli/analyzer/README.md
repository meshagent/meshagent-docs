# MeshAgent Quickstart: Analyzer

Create a chat-based agent that can analyze documents in a room, write code, and generate helpful insights. You can either run it locally from the MeshAgent CLI or deploy it as a persistent service in MeshAgent Studio.

## Prerequisites
- MeshAgent account, sign up at [www.meshagent.com](https://www.meshagent.com)
- MeshAgent CLI installed (`uv add "meshagent[all]"`)

## What's included
- `meshagent.yaml` for deploying the agent as a MeshAgent service (uses a public image)

## Option 1: Run Locally
Use this when you want to try the agent without deploying a service. The CLI spins up the agent directly, and it will appear in the room you join for as long as the command is running.

Open your terminal and run the following: 
```bash
meshagent setup
meshagent chatbot join \
  --room=myroom \
  --agent-name=analyzer \
  --model=codex-mini-latest \
  --local-shell \
  --toolkit=ui \
  --rule='you may only write files inside the /data folder, everything else is read only. You should use the display_document tool to show files to users. If the user asks for a chart, install matplotlib and use it to make a chart image. strip the leading /data when showing files with display_document since the display_document tool expects a path relative to /data. If the user mentions a file that they uploaded, it should be inside the /data folder since the root of the room storage is mounted to /data.'
```

Now that the agent is running, head to [MeshAgent Studio](https://studio.meshagent.com) to try it out!
1. Open your room (e.g., `myroom`)
2. Under the **Participants** tab select ``analyzer`` and begin working with the agent

When you run the analyzer from the CLI the agent will write files to your local disk under `/data`. You can explore them with:

```bash
cd data
ls
```

## Option 2: Deploy the agent as a service in MeshAgent Studio
Use this when you want the agent to be always available in a room or project. No Dockerfile needed; the YAML points to a maintained public image.

```
meshagent service create --file=meshagent.yaml --room=myroom 
```

- --room is optional. Without it, the service is deployed at the project level and appears in all rooms in your project.
- After it’s live, open the target room in [MeshAgent Studio](https://studio.meshagent.com) and start chatting with `analyzer`.

---

## Learn more at: 

**Website**: www.meshagent.com(https://www.meshagent.com)
**Documentation**: docs.meshagent.com(https://docs.meshagent.com/)
