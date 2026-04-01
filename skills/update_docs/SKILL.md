---
name: update-docs
description: |
  Update and create MeshAgent documentation to keep it accurate and in sync with the SDK and CLI source code.
  Use this skill whenever: a pull request has merged or code changed and the docs need updating; the user asks to update, create, reorganize, or improve any documentation page; the user says docs are stale or mentions a feature that needs documenting; you're reviewing docs for accuracy against the actual implementation.
  Always use this skill for any MeshAgent documentation task — the codebase evolves quickly and this skill contains the rules that keep docs trustworthy, useful, and aligned with the current docs style.
---

# MeshAgent Documentation Skill

Always assume the current documentation may be stale. The SDK and CLI source code is the source of truth. Read the actual implementation before writing or updating anything.

## Repo layout

All source code lives under `meshagent-sdk/` and documentation under `meshagent-sdk/meshagent-docs/`. When you need to find something, explore the repo — don't rely on a static map. Key things to know:

- SDK implementations are in `meshagent-sdk/meshagent-agents/` (Python), `meshagent-sdk/meshagent-cli/` (CLI), `meshagent-sdk/meshagent-js/`, `meshagent-sdk/meshagent-ts/`, `meshagent-sdk/meshagent-dart/`, `meshagent-sdk/meshagent-dotnet/`, and `meshagent-sdk/meshagent-api/`
- Doc source examples go in `meshagent-sdk/meshagent-docs/examples/` when the example is substantial or reusable
- `meshagent-sdk/meshagent-docs/snippets/examples/` is auto-generated — never hand-edit it
- `meshagent-sdk/meshagent-docs/docs.json` controls navigation — update it when adding, removing, or regrouping pages
- The `archive/` folders under `examples/` contain old examples; don't reference them in new docs

## Source of truth

- Read the actual CLI and SDK implementation before describing any capability.
- Prefer current first-class docs and current example files over anything in `archive/`.
- Treat generated docs (like CLI help pages in `reference/meshagent_cli_help`) separately — do not hand-edit them, they are produced by `build_cli_help.py`.

## Docs tone and style

MeshAgent docs should feel:

- **clear and direct** — short sentences, plain definitions, minimal jargon
- **room-centered** — treat the room as the runtime and collaboration boundary when writing high-level docs
- **product-shaped** — explain MeshAgent in terms of projects, rooms, agents, services, Studio, Powerboards, CLI, SDKs, and APIs
- **honest but persuasive** — overview pages should help a reader understand why MeshAgent is valuable, but they should sell through specificity rather than hype
- **concrete about surfaces** — say where a user does something: MeshAgent Studio, Powerboards, CLI, SDK, or REST API
- **inclusive of both starting paths** — mention built-in agents and no-code starts when relevant, while also supporting users who want to build or bring their own agents, tools, and services

When relevant, distinguish:

- **MeshAgent Studio** as the developer/operator interface
- **Powerboards** as the end-user interface
- both as surfaces over the same underlying projects and rooms

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
3. Check what already exists in the docs to avoid duplication and stay consistent in tone, navigation, and IA.
4. Identify the page's job before writing: overview, key concepts, architecture, quickstart, how-to, API reference, or compatibility page.
5. Make the changes following the page type standards and writing rules below.

## Writing rules

- Write for the actual audience of the page. Many pages are for developers, but overview, quickstart, interfaces, and onboarding pages may also be read by end users, evaluators, or buyers.
- Lead with capabilities and workflows, not migration context.
- Explain what a feature does, why it matters, and how a user actually uses it.
- For overview pages, explain what MeshAgent is, what it enables, and why someone would care before going deep into sub-features.
- Prefer positive framing: define what MeshAgent is before comparing it to other categories.
- Keep the room at the center of high-level product explanations.
- No filler pages. Every page must answer a real question a developer would have. If the content doesn't justify a standalone page, make it a section in an existing page.
- Avoid internal framing: don't write about how the architecture changed, what things used to be called, or "under the covers" implementation details unless they directly help the user.
- Avoid vague phrasing when a more concrete explanation is available. Say `meshagent process`, `MeshAgent Studio`, `Powerboards`, `room`, or `project` instead of hiding behind abstract language.
- Do not overuse implementation adjectives like "process-backed" on high-level pages when "agent" or "`meshagent process` agent" is clearer.
- If a concept page is primarily conceptual, it does not need code just to justify itself. Add code when the page teaches a workflow or usage pattern.

For agent-related docs specifically, read `references/codebase-context.md` before writing — it covers the current runtime patterns and which older ones to avoid teaching.

## Page types

Read `references/page-types.md` for detailed templates. Here's a quick guide:

### Overview page
For high-level product or section landing pages:
- What is this?
- Why does it matter?
- What does it enable?
- What are the core surfaces or concepts?
- Where should the reader go next?

### Key concepts page
For glossary-style definitions:
- Define the main terms simply
- Keep the entries short
- Add strong cross-links to the deeper pages

### Architecture page
For system-shape explanations:
- How do the main surfaces fit together?
- What are the important boundaries?
- What mental model should the reader keep in mind?

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

Prefer source examples in `examples/` plus generated snippet imports for substantial or reusable examples.

Short inline commands or tiny illustrative snippets are acceptable directly in `.mdx` when they are clearer than a snippet import and do not need reuse. Multi-line examples, YAML configs, SDK snippets, and reusable walkthrough code should live in `examples/`.

A build step (`build-examples.js`) converts source files in `examples/` to `.mdx` snippets in `snippets/examples/`. In doc pages, import and render the snippet.

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
- If you changed navigation or page grouping, read the surrounding section in `docs.json` to make sure the IA still makes sense
- If you added new examples, confirm `node build-examples.js` ran and the snippet exists in `snippets/examples/`
