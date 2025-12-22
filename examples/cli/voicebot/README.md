# MeshAgent Quickstart: VoiceBot

Spin up a voice-enabled agent that listens and speaks in your room. You can run it locally for quick trials or deploy it as a persistent service in MeshAgent Studio.

## Prerequisites
- A GitHub repo containing this example (Dockerfile + service template)
- A MeshAgent account, you can sign up at [www.meshagent.com](https://www.meshagent.com)

## What's included
- `meshagent.yaml` for deploying the agent as a MeshAgent service (uses a public image)

### Option 1: Run Locally
Use this when you want to try the agent without deploying a service. The CLI spins up the agent directly, and it will appear in the room you join for as long as the command is running.

Open your terminal and run:
```bash
meshagent setup
meshagent voicebot join --agent-name=voicebot --room=myroom 
```
Now that the agent is running, head to [MeshAgent Studio](https://studio.meshagent.com) to try it out!
1. Open your room (e.g., `myroom`)
2. Under the **Participants** tab select ``voicebot`` and begin talking to the agent! We recommend muting yourself once you are done speaking so that the agent doesn't pick up on background noise and get interrupted.

## Option 2: Deploy the agent as a service in MeshAgent Studio
Use this when you want the agent to be always available in a room or project. No Dockerfile needed; the YAML points to a maintained public image.

```
meshagent service create --file=meshagent.yaml --room=myroom 
```

- --room is optional. Without it, the service is deployed at the project level and appears in all rooms in your project.
- After it’s live, open the target room in [MeshAgent Studio](https://studio.meshagent.com) and start chatting with `voicebot`.

---
## For more information see: 

**Website**: www.meshagent.com(https://www.meshagent.com)
**Documentation**: docs.meshagent.com(https://docs.meshagent.com/)
