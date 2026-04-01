# Page Type Templates

Reference templates and guidance for each type of MeshAgent documentation page. Pick the type that matches the job the page needs to do — don't force content into the wrong shape.

---

## 1. Concept / Overview

Use when the goal is orientation: what is this feature, why does it matter, and where do you go next? These pages are the entry point to a feature area, not the exhaustive reference.

**Structure:**
```
## Overview / What is X?
<Plain-language explanation. 2–4 sentences. No jargon without definition.>

## How X fits into MeshAgent
<How this connects to the rest of the system — rooms, agents, services, etc.>

## When to use it
<Decision guidance: when is this the right tool vs. alternatives?>

## Where to start
<Short bulleted list of links to the relevant how-to, quickstart, and reference pages.>
```

**Checklist:**
- Doesn't try to explain everything — leaves depth to dedicated pages
- Has clear "where to start" links so the reader knows where to go next
- No raw code inline unless a single short command illustrates the concept

---

## 2. API Reference

Use for documenting a specific API surface (e.g., `DatabaseClient`, `MemoryClient`, `StorageClient`). These are the canonical source for what the API can do and how to call it.

**Structure:**
```
## Overview
<1–3 sentences: what is this API and what problem does it solve.>

## Why use the X API?
<Specific advantages — what makes this the right choice.>

## How it works
<Mental model before the method list. Note important constraints or behaviors.>

## Permissions and grants
<If this API requires grants, explain what's needed and link to scopes/packaging.>

## CLI and SDK availability
<Which CLI commands and which SDKs (Python, JS/TS, Dart, .NET) support this.>

## API Methods
<For each method: description, parameters with types, return value, example via snippet import.>

## Related guides
<Links to concept overview, related APIs, packaging if grants are needed.>
```

**Checklist:**
- Each method has: description, parameters with types, return value, and an example
- Examples use snippet imports, not inline code
- CLI example shown alongside SDK examples where the CLI supports it
- Permissions section present if the API requires grants

---

## 3. Quickstart

Use to get the reader from zero to something working as fast as possible. These are hands-on and step-by-step. Not a reference — a guided first run.

**Structure:**
```
<Brief intro: what the reader will build or accomplish, and what they'll learn.>

## Prerequisites
<What they need before starting: CLI installed, account set up, etc.>

## Step 1: ...
## Step 2: ...
...

## What's next
<Links to deepen understanding: concept guide, full API reference, more examples.>
```

**Checklist:**
- Steps are numbered and sequential — the reader should be able to follow along exactly
- Concrete and runnable — no placeholders like `<your value here>` without explanation
- Code examples via snippet imports
- Doesn't over-explain — gets the reader to a working result and then points them elsewhere

---

## 4. How-to / Deployment Guide

Use for specific tasks: deploying a service, setting up a channel, connecting an integration. More focused than a quickstart (assumes the reader has context) and more prescriptive than a concept guide.

**Structure:**
```
## Overview
<One paragraph: what this guide accomplishes and when you'd use this pattern.>

## Prerequisites
<What's needed before starting.>

## Step 1: ...
## Step 2: ...
...

<Optional: variation or next-level configuration if relevant.>
```

**Checklist:**
- Clear scope: the reader should know exactly what they'll have at the end
- Deployment examples always use CLI; show `meshagent mailbox create` before mail examples
- Code examples via snippet imports (especially YAML configs and shell sequences)

---

## 5. Named Agent / Service Page

Use for documenting a specific packaged agent or service (e.g., Voice Agent, Document Author, Browser). These combine a brief concept explanation with setup and usage.

**Structure:**
```
## Overview
<What this agent does, what it's for, when you'd deploy it.>

## How it works
<Brief description of what makes this agent tick — tools it uses, channels it supports, etc.>

## Deploy
<CLI commands to deploy it. Use snippet imports for YAML configs.>

## Usage
<How to interact with it once deployed — CLI invocation, chat, mail, etc.>

## Configuration / Options
<Key config parameters, optional channels, or environment variables if relevant.>

## Related
<Links to related agents, tools, or concept pages.>
```

**Checklist:**
- Concrete deployment commands (don't describe in the abstract)
- Examples show real invocation, not pseudo-code
- Links to any tools or services this agent depends on

---

## 6. Architecture / Deep Dive

Use when the reader needs to understand *how* something works internally — not just how to use it. Common for complex runtimes (e.g., Process Agent Architecture, Threads Overview).

**Structure:**
```
## Overview
<What this page explains and why understanding it matters.>

## <Core concept 1>
<Explanation with diagrams or ASCII art if helpful.>

## <Core concept 2>
...

## Implications for your code
<Practical takeaways: how this architecture affects what the reader writes or configures.>

## Related
<Links to the concept overview and API reference for this feature area.>
```

**Checklist:**
- Starts from the reader's perspective (what do I need to understand, and why?)
- Concrete examples where they help, but this page is allowed to stay mostly prose
- Doesn't duplicate content from the concept overview or API reference pages

---

## 7. Integration Guide

Use for connecting MeshAgent to a specific third-party service (e.g., Supabase MCP, OpenAI Connectors, Firebase). Focused on the integration-specific setup.

**Structure:**
```
## Overview
<What this integration enables and why you'd use it.>

## Prerequisites
<What's needed on both the MeshAgent side and the third-party side.>

## Setup
<Step-by-step: credentials, config, deploy. CLI and YAML examples via snippet imports.>

## Usage
<How to use the integration once it's running.>

## Related
<Links to the third-party docs and relevant MeshAgent pages.>
```

---

## 8. Archived / Compatibility Reference

Use for documenting patterns that existed in older versions but are no longer the recommended path. These help users who encounter old code or docs understand what they're looking at.

**Structure:**
```
<Callout or note at the top: "This page documents a legacy pattern. [Link to current alternative] is the recommended approach.">

## What this was
<Brief explanation of what the old pattern did.>

## Migration
<How to move to the current pattern, with before/after examples.>
```

**Checklist:**
- Never present the archived pattern as recommended
- Always link prominently to the current alternative at the top
- Keep these out of the main navigation user journey unless specifically requested

---

## Avoiding filler pages

Before creating a new page, ask: does this answer a real question a developer would search for? Signs a page is filler:
- It's just a short intro with nothing but links to other pages
- Its content duplicates what another page already says
- It describes something with migration context instead of user-facing value
- It exists as an "overview" but there's only one sub-page under it

When in doubt, fold the content into a neighboring page rather than creating a new one.
