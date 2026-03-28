# MeshAgent Process Sample: Mail Channel

Run one process-backed agent with a mail channel.

Use this sample when the same long-running agent should receive email through a mailbox and reply through the mail flow.

## Prerequisite

Create the mailbox first:

```bash
meshagent mailbox create \
  --address=support-agent@mail.meshagent.com \
  --room=myroom \
  --queue=support-agent@mail.meshagent.com
```

## Local run

```bash
meshagent setup

meshagent process join \
  --room=myroom \
  --agent-name=support-agent \
  --channel=mail:support-agent@mail.meshagent.com \
  --require-storage \
  --require-web-search \
  --room-rules="agents/support-agent-mail/rules.txt" \
  --rule="You are a helpful support agent. Reply clearly by email, save important attachments or artifacts to storage, and use web search when needed."
```

## Deploy

```bash
meshagent service create-template --file=meshagent.yaml --room=myroom --value email_address=support-agent@mail.meshagent.com
```
