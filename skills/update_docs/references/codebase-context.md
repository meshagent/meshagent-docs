# MeshAgent Codebase Context

This document describes the current state of the MeshAgent runtime and codebase. Use it as background when writing or reviewing agent-related documentation — it tells you which patterns are current, which are legacy, and how to handle each.

---

## Current runtime: `meshagent process`

The primary, recommended runtime for MeshAgent agents is `meshagent process`. It's a single process that can handle multiple interaction channels:

- `chat` — chat interface in a room
- `mail:EMAIL` — email via a mailbox
- `queue:NAME` — queue-based or scheduled task
- `toolkit:NAME` — tool invocations from other agents or clients

When documenting agents, default to `meshagent process` as the entry point. Show examples with CLI commands like `meshagent process join`.

For deployment examples that include mail, always show `meshagent mailbox create` before the `meshagent process` command — the mailbox must exist first.

For advanced SDK use cases, `SingleRoomAgent` is the entry point for building custom room-connected agents in Python. Mention it when the topic is specifically about SDK-level agent authoring.

---

## Interfaces: MeshAgent Studio and Powerboards

When writing high-level docs, keep the interface split clear:

- **MeshAgent Studio** is the main developer/operator interface for building, testing, deploying, inspecting, and administering
- **Powerboards** is the main end-user interface for using built-in and deployed agents in rooms
- both interfaces connect to the same underlying projects and rooms

If a page is about onboarding, interfaces, or product overview, explain where the user would do the task and whether the task is more developer-oriented or end-user-oriented.

---

## Legacy runtimes (do not teach in first-class docs)

The following older runtime types exist in the codebase for compatibility but should not be taught to new users or presented as recommended patterns in first-class documentation:

| Old runtime | Replacement |
|-------------|-------------|
| `ChatBot` | `meshagent process` with `chat` channel |
| `Worker` | `meshagent process` with `queue:NAME` channel |
| `MailBot` | `meshagent process` with `mail:EMAIL` channel |
| `TaskRunner` | `meshagent process` with `queue:NAME` channel |

**In docs**: Don't use these class names in new examples or explanations. If they appear in existing docs you're updating, replace them with the `meshagent process` equivalent unless the page is explicitly a compatibility reference.

**In archive**: The `examples/archive/` folder contains old examples using these runtimes. Leave them there but don't link to them from first-class docs.

---

## Stale CLI commands to grep for

When reviewing or updating docs, grep for these commands in first-class doc pages — they indicate outdated content:

- `meshagent chatbot`
- `meshagent worker`
- `meshagent mailbot`
- `meshagent task-runner`

If found in non-archive docs, replace with the equivalent `meshagent process` command or remove the stale example.

---

## Container image for CLI examples

Use `meshagent/cli:default` as the container image in CLI-based deployment examples.

---

## What this means for documentation work

- When you encounter an old runtime name in a doc you're editing, update it to the current pattern.
- When writing a new getting-started or overview page, show `meshagent process` — not the older runtimes.
- If a page needs to mention the older runtimes for historical or compatibility reasons, frame them as compatibility surfaces, not recommended paths.
- Archive content can keep its original terminology. Don't update archive pages unless the user explicitly asks.
