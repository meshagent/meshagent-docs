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
- The `archive/` folders under `examples/` contain old examples; don't reference them in new docs

## Source of truth

- Read the actual CLI and SDK implementation before describing any capability.
- Treat generated docs (like CLI help pages in `reference/meshagent_cli_help`) separately — do not hand-edit them, they are produced by `build_cli_help.py`.

## Docs tone and style

MeshAgent docs should feel:

- **clear and direct** — short sentences, plain definitions, minimal jargon
- **room-centered** — treat the room as the runtime and collaboration boundary when writing high-level docs
- **product-shaped** — explain MeshAgent in terms of projects, rooms, agents, services, Studio, Powerboards, CLI, SDKs, and APIs
- **honest but persuasive** — overview pages should help a reader understand why MeshAgent is valuable, but they should sell through specificity rather than hype
- **concrete about surfaces** — say where a user does something: MeshAgent Studio, Powerboards, CLI, SDK, or REST API
- **inclusive of both starting paths** — mention built-in agents and no-code starts when relevant, while also supporting users who want to build or bring their own agents, tools, and services

MeshAgent docs should also be:

- **actionable first** — get to the command, UI path, or decision the reader actually needs
- **light on prose** — explain critical concepts, but do not add narrative that does not help the reader choose a path or complete a task
- **non-redundant** — if nearby pages already explain a concept clearly, link instead of repeating the same explanation
- **few-page by default** — prefer fewer stronger pages over many thin or overlapping pages

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
5. **Create new pages for genuinely new concepts** — if the PR introduces something new enough to warrant its own page (a new API surface, a new runtime concept, a new major CLI subcommand), create it. See "Page types in practice" below. Update `docs.json` to add it to the navigation.

### Mode 2: User-requested (help with specific docs work)

When the user asks to update, write, reorganize, or review docs:

1. Clarify the scope if needed — which section, concept, or page?
2. Read the relevant SDK/CLI source for the thing being documented. Never document from memory.
3. Check what already exists in the docs to avoid duplication and stay consistent in tone, navigation, and IA.
4. Identify the page's job before writing. In practice, most MeshAgent pages should be one of the small set described in "Page types in practice" below.
5. Make the changes following the page type standards and writing rules below.

## Writing rules

- Write for the actual audience of the page. Many pages are for developers, but overview, quickstart, interfaces, and onboarding pages may also be read by end users, evaluators, or buyers.
- Lead with capabilities and workflows, not migration context.
- Explain what a feature does, why it matters, and how a user actually uses it.
- For overview pages, explain what MeshAgent is, what it enables, and why someone would care before going deep into sub-features.
- Prefer positive framing: define what MeshAgent is before comparing it to other categories.
- Keep the room at the center of high-level product explanations.
- No filler pages. Every page must answer a real question a developer would have. If the content doesn't justify a standalone page, make it a section in an existing page.
- Prefer fewer pages. Do not split content into multiple pages unless the split makes the docs easier to follow and avoids a crowded page with two distinct jobs.
- Do not repeat the same concept summary in bullets, tables, and intro paragraphs on the same page. Pick one strong explanation and move on.
- On workflow pages, do not spend multiple paragraphs explaining what the page is for. State the outcome, orient the reader briefly, then show the path.
- On concept pages, keep definitions short and grounded in what the reader will touch in the product, CLI, SDK, or API.
- Avoid internal framing: don't write about how the architecture changed, what things used to be called, or "under the covers" implementation details unless they directly help the user.
- Avoid vague phrasing when a more concrete explanation is available. Say `meshagent process`, `MeshAgent Studio`, `Powerboards`, `room`, or `project` instead of hiding behind abstract language.
- Do not overuse implementation adjectives like "process-backed" on high-level pages when "agent" or "`meshagent process` agent" is clearer.
- If a concept page is primarily conceptual, it does not need code just to justify itself. Add code when the page teaches a workflow or usage pattern.
- Prefer CLI examples where the CLI is the main real-world path. Add UI steps when the task is commonly done in Studio or Powerboards.
- Use section headings that help the reader choose or do something. Avoid vague headings like "use this page", "short version", or "choose between them" unless they are truly necessary.

For agent-related docs specifically, read `references/codebase-context.md` before writing — it covers the current runtime patterns and which older ones to avoid teaching.

## Page types in practice

Read `references/page-types.md` for the full guidance. In practice, most MeshAgent docs should be one of these:

### 1. Section guide
Use for section-leading pages such as Projects, Observability, Services, or a top-level product surface.

- Explain what the area is in plain language
- Define only the concepts the reader needs right now
- Link clearly to the next pages they should read
- Keep these pages compact; do not turn them into soft marketing overviews

### 2. Quickstart or task guide
Use for pages that help the reader do something: deploy a service, connect an MCP server, create a room, configure OAuth, or start an agent.

- Lead with the outcome
- Show the main path quickly
- Include only the concept explanation needed to support the steps
- Prefer one page with a few clear paths over several overlapping pages

### 3. Reference
Use for dense documentation such as Room APIs, service manifest fields, CLI command reference, SDK/package overview, or auth/access details.

- Start with a brief plain-language orientation
- Organize for lookup, not for narrative reading
- Be precise and avoid filler
- Link back to the right guide when a reader needs workflow context

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
- Read the page top to bottom as a new user and remove any repeated framing, redundant bullets/tables, or headings that do not help the reader act
