# Examples Reorganization Plan

## Goals

- Make `examples/` the source of truth for runnable example assets.
- Stop pasting full YAML manifests directly into docs pages.
- Keep example paths easy to understand without forcing them to mirror the docs navigation.
- Separate language-specific code examples from YAML-first CLI/service examples.

## Directory conventions

Use these top-level example buckets:

- `examples/cli/`
- `examples/python/`
- `examples/javascript/`
- `examples/typescript/`
- `examples/dart/`
- `examples/dotnet/`

Within `examples/cli/`:

- use top-level folders for concrete scenarios and use cases
- use `examples/cli/concepts/` for focused concept examples that demonstrate one feature in isolation

Examples:

- `examples/cli/chatbot/`
- `examples/cli/supabase-mcp/`
- `examples/cli/process-news-agent/`
- `examples/cli/concepts/use-project-secrets/`
- `examples/cli/concepts/use-room-secrets/`
- `examples/cli/concepts/use-installer-secrets/`

## Snippet policy

- Full YAML manifests should not appear inline in docs pages.
- Every full YAML manifest shown in docs should have a backing file in `examples/`.
- Docs pages should import snippet files from `snippets/examples/...`.
- Small YAML fragments are still allowed inline when they explain a field or subsection rather than a full runnable manifest.

Current limitation:

- the current snippet layer is plain MDX, not a live file renderer
- snippet files still need to be kept in sync with the backing example file

Recommended follow-up:

- add a generation or verification step so snippet YAML stays synchronized with `examples/`

## Migration phases

### Phase 1: Establish conventions

- Adopt the top-level `examples/{cli,python,javascript,typescript,dart,dotnet}` structure.
- Treat `examples/cli/concepts/` as the home for concept-only YAML examples.
- Update `examples/cli/README.md` to explain scenario folders vs concept folders.

### Phase 2: Migrate secrets examples

- Add:
  - `examples/cli/concepts/use-project-secrets/`
  - `examples/cli/concepts/use-room-secrets/`
  - `examples/cli/concepts/use-installer-secrets/`
  - `examples/cli/concepts/use-image-pull-secrets/`
- Add matching snippet wrappers under `snippets/examples/cli/concepts/...`
- Replace inline YAML in the secrets docs with imported snippets.

### Phase 3: Audit current YAML examples

- Inventory all files in `examples/cli/` and `examples/packaging/`.
- Record:
  - backing example file
  - matching snippet file
  - docs pages that import the snippet
  - whether the example is a scenario, concept, duplicate, or orphan

### Phase 4: Collapse `examples/packaging/` into `examples/cli/`

Migrate packaging examples into scenario or concept folders under `examples/cli/`.

Examples:

- `examples/packaging/process_agent_service.yaml` -> `examples/cli/process-news-agent/meshagent.yaml`
- `examples/packaging/mcp_supabase/*` -> `examples/cli/supabase-mcp/`
- `examples/packaging/service_chatbot.yaml` -> `examples/cli/concepts/use-service/meshagent.yaml`
- `examples/packaging/service_template_chatbot.yaml` -> `examples/cli/concepts/use-service-template/meshagent.yaml`

### Phase 5: Add tooling

- Add a script or check that verifies imported snippet YAML matches the file in `examples/`.
- Add a simple audit for orphaned example files and missing snippet wrappers.

## Practical rules for authors

- If the doc shows a full manifest, create the file in `examples/` first.
- If the manifest is only meant to explain one feature and is not a full workflow, place it under `examples/cli/concepts/`.
- If the manifest supports a concrete end-to-end workflow, place it in a scenario folder under `examples/cli/`.
- Keep README files next to CLI examples when the folder contains more than one asset or needs setup steps.
