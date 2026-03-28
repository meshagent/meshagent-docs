# MeshAgent Process Sample: Queue Channel

Run one process-backed agent with a queue channel.

Use this sample when background jobs should be pushed into the agent through a room queue.

## Local run

```bash
meshagent setup

meshagent process join \
  --room=myroom \
  --agent-name=queue-agent \
  --channel=queue:support-jobs \
  --require-storage \
  --require-web-search \
  --rule="You are a queue-based support operations agent. Process queued jobs without asking follow-up questions unless the job explicitly asks for interactive behavior."
```

Send work into the queue:

```bash
meshagent room queue send \
  --room=myroom \
  --queue=support-jobs \
  --json '{"prompt":"Summarize the latest support backlog and save a report."}'
```

## Deploy

```bash
meshagent service create --file=meshagent.yaml --room=myroom
```
