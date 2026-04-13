# MeshAgent Process Sample: Chat Channel

Run one process-backed agent with a chat channel.

Use this sample when you want:

- a room-visible agent participants can message directly
- thread-aware chat behavior
- a process runtime that can later grow into queue, mail, or toolkit channels

## Local run

```bash
meshagent setup

meshagent process join \
  --room=myroom \
  --agent-name=support-agent \
  --channel=chat \
  --threading-mode=default-new \
  --thread-dir=".threads/support-agent" \
  --web-search \
  --storage \
  --room-rules="agents/support-agent/rules.md" \
  --rule="You are a helpful support agent. Answer clearly, use web search when needed, and save important artifacts to storage."
```

## Deploy

```bash
meshagent service create --file=meshagent.yaml --room=myroom
```
