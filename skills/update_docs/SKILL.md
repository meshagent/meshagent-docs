---
name: update-docs
description: Update and create MeshAgent and Powerboards documentation and examples.
---

# Update docs

Always assume the current documentation may be stale. Use the MeshAgent SDK and CLI implementation as the source of truth when updating docs and examples.

## Source of truth

- Check the actual CLI and SDK implementation before describing a capability.
- Prefer current first-class docs and current example files over older archived material.
- Treat generated docs such as CLI help separately. Do not hand-edit them unless that is explicitly the task.

## Primary product story

- Default to `meshagent process` as the main runtime for MeshAgent agents.
- Explain `meshagent process` in terms of what it does, what channels it supports, what it enables, and when to use it.
- Present channels as part of one process-backed agent:
  - `chat`
  - `mail:EMAIL`
  - `queue:NAME`
  - `toolkit:NAME`
- When a getting-started or overview example includes mail, always show `meshagent mailbox create` before the `meshagent process` command.
- Prefer examples that show one agent growing across channels instead of switching between older runtime types.

## Writing rules

- Write for end users of MeshAgent, not for internal architecture discussions.
- Lead with capabilities and workflows, not migration context.
- Explain what a feature does, why it matters, and how a user actually uses it.
- Avoid internal framing such as:
  - “the most important thing is not X but Y”
  - “the architecture itself changed”
  - “under the covers”
  - migration narration that does not help the user complete a task
- Prefer plain product language over internal runtime language when possible.
- Do not call something a “process-backed chat agent” when the page is really about a broader process-backed agent. Only narrow to chat when the example specifically depends on the chat channel.

## Examples

- Prefer CLI examples for user-facing docs unless the task is specifically about SDK authoring.
- Use `meshagent/cli:default` for CLI container image examples.
- Keep examples concrete and runnable.
- When documenting mail workflows, tell the reader to email the agent after setting up the mail channel.
- When documenting toolkit channels, include the actual CLI flow for invoking the agent through `meshagent room agent invoke-tool` if the page is about that capability.
- When documenting deployment, prefer deploying the same shape the reader just tested locally.

## SDK alignment

- For Python docs, treat `meshagent process` as the main documented runtime path.
- `SingleRoomAgent` is the advanced SDK entry point for custom room-connected agents.
- Mention older compatibility classes like `ChatBot`, `Worker`, `MailBot`, and `TaskRunner` only when documenting compatibility or reference surfaces, not as the recommended path for new users.
- Archive material can retain old terminology, but first-class docs should not teach those older runtimes.

## Information architecture

- Keep one clear primary page for `meshagent process` rather than spreading the same explanation across several redundant pages.
- Archive content should exist only to preserve old material temporarily. Do not keep archive docs in the main user journey unless explicitly requested.
- Remove dead or redundant pages from nav when their content has been folded into stronger pages.

## Validation

Before finishing:

- grep for stale command examples such as `meshagent chatbot`, `meshagent worker`, `meshagent mailbot`, and `meshagent task-runner` in first-class docs
- grep for links to deleted pages
- run `git diff --check`
- validate `meshagent-sdk/meshagent-docs/docs.json` with `jq empty`
