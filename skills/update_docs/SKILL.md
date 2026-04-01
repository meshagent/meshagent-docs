---
name: update-docs
description: |
  Update and create MeshAgent documentation to keep it accurate and in sync with the SDK and CLI source code.
  Use this skill whenever: a pull request has merged or code changed and the docs need updating; the user asks to update, create, reorganize, or improve any documentation page; the user says docs are stale or mentions a feature that needs documenting; you're reviewing docs for accuracy against the actual implementation.
  Always use this skill for any MeshAgent documentation task — the codebase evolves quickly and this skill contains the rules that keep docs trustworthy and useful.
---

# MeshAgent Documentation Skill

Always assume the current documentation may be stale. The SDK and CLI source code is the source of truth. Read the actual implementation before writing or updating anything.

## Repo layout

All source code lives under `meshagent-sdk/` and documentation under `meshagent-sdk/meshagent-docs/`. When you need to find something, explore the repo — don't rely on a static map. Key things to know:

- SDK implementations are in `meshagent-sdk/meshagent-agents/` (Python), `meshagent-sdk/meshagent-cli/` (CLI), `meshagent-sdk/meshagent-js/`, `meshagent-sdk/meshagent-dart/`, `meshagent-sdk/meshagent-dotnet/`
- Doc source examples go in `meshagent-docs/examples/` (not in the `.mdx` files directly — see "Code examples" below)
- `meshagent-docs/snippets/examples/` is auto-generated — never hand-edit it
- `meshagent-docs/docs.json` controls navigation — update it when adding or removing pages
- The `archive/` folders under `examples/` contain old examples; don't reference them in new docs

## Source of truth

- Read the actual CLI and SDK implementation before describing any capability.
- Prefer current first-class docs and current example files over anything in `archive/`.
- Treat generated docs (like CLI help pages in `reference/meshagent_cli_help`) separately — do not hand-edit them, they are produced by `build_cli_help.py`.

## Two modes of operation

### Mode 1: PR-triggered (code changed → update docs)

When a PR has merged or the user shares code changes:

1. **Find what changed** — use `git log` and `git diff HEAD~1` (or the PR diff the user shares) to identify changed files in the SDK and CLI.
2. **Understand the change** — read the changed source files. Look for: new functions, methods, or classes; changed signatures or behavior; new CLI commands or flags; removed or deprecated things.
3. **Search the docs** — grep for the affected class names, method names, and CLI commands across `meshagent-docs/`. Find every page that references what changed.
4. **Update affected pages** — correct descriptions, signatures, and behaviors. If examples are affected, update the source in `examples/` first (see "Code examples" below), then run the build.
5. **Create new pages for genuinely new concepts** — if the PR introduces something new enough to warrant its own page (a new API surface, a new runtime concept, a new major CLI subcommand), create it. See "Page types" below. Update `docs.json` to add it to the navigation.

### Mode 2: User-requested (help with specific docs work)

When the user asks to update, write, reorganize, or review docs:

1. Clarify the scope if needed — which section, concept, or page?
2. Read the relevant SDK/CLI source for the thing being documented. Never document from memory.
3. Check what already exists in the docs to avoid duplication and stay consistent in tone.
4. Make the changes following the page type standards and writing rules below.

## Writing rules

- Write for developers using MeshAgent, not for internal architecture discussions.
- Lead with capabilities and workflows, not migration context.
- Explain what a feature does, why it matters, and how a user actually uses it.
- No filler pages. Every page must answer a real question a developer would have. If the content doesn't justify a standalone page, make it a section in an existing page.
- Avoid internal framing: don't write about how the architecture changed, what things used to be called, or "under the covers" implementation details unless they directly help the user.

For agent-related docs specifically, read `references/codebase-context.md` before writing — it covers the current runtime patterns and which older ones to avoid teaching.

## Page types

Read `references/page-types.md` for detailed templates. Here's a quick guide:

### Concept guide
For explaining what something is and why it matters:
- What is it (plain language)?
- Why does it matter / when would you use it?
- How does it work at a conceptual level?
- Links to related API reference and examples

### API reference page (e.g., Room Database API, Room Memory API)
- Brief overview: what is this and what does it do?
- When to use it
- How it works (mental model, not just a method list)
- CLI and SDK availability note
- Each method: description, parameters, return value, example
- Related guides links at the bottom

### Complex concept with multiple components (e.g., Process Agent)
When something has many moving parts, consider a conceptual overview page plus separate deep-dive pages:
- Overview page: what is it, what are its components, when to use it, how to deploy
- Always include CLI commands for deployment and usage flows
- Show CLI examples wherever possible; SDK examples for SDK-specific features

## Code examples

**Do not write raw code directly in `.mdx` files.**

All code examples live in `examples/`. A build step (`build-examples.js`) converts them to `.mdx` snippets in `snippets/examples/`. In doc pages, import and render the snippet.

Read `references/examples-workflow.md` for the full pipeline, file conventions, and import syntax.

### Quick reference — importing a snippet

```mdx
import MyExample from "/snippets/examples/cli/my-feature/meshagent.mdx"

<CodeGroup>
  <MyExample />
</CodeGroup>
```

## Validation

Before finishing any doc update:

- Grep for stale command examples in first-class docs (see `references/codebase-context.md` for the list)
- Grep for links to deleted pages
- Run `git diff --check`
- Validate `docs.json` with `jq empty meshagent-sdk/meshagent-docs/docs.json`
- If you added new examples, confirm `node build-examples.js` ran and the snippet exists in `snippets/examples/`
