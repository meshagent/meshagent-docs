# MeshAgent Process Sample: Toolkit Channel

Run one process-backed agent with a toolkit channel.

Use this sample when other agents should call the agent like a tool instead of treating it mainly as a room participant.

## Local run

```bash
meshagent setup

meshagent process join \
  --room=myroom \
  --agent-name=research-helper \
  --channel=toolkit:research-helper \
  --require-web-search \
  --require-storage \
  --rule="You are a callable research helper. Produce concise results, cite sources when possible, and save larger artifacts to storage."
```

## Deploy

```bash
meshagent service create --file=meshagent.yaml --room=myroom
```
