# CLI Examples

`examples/cli/` contains YAML-first examples that use MeshAgent CLI entrypoints and public CLI images.

Use this directory for two kinds of examples:

- **Scenario examples** at the top level, such as `process-news-agent/`, `voicebot/`, or `supabase-mcp/`
- **Concept examples** under `concepts/`, such as `concepts/use-room-secrets/`

## What belongs here

Put an example under `examples/cli/` when:

- the main artifact is a YAML manifest
- the runtime is a MeshAgent CLI image
- the doc is teaching how to package, deploy, or wire a CLI-based service

Use language-specific directories like `examples/python/` when the code itself is the main thing being taught.

## Folder conventions

Each scenario or concept folder should contain:

- `meshagent.yaml` for the primary manifest
- `README.md` when setup steps or supporting context are needed
- optional helper assets such as `rules.md`, `start.sh`, or extra YAML files

Examples:

- `examples/cli/process-news-agent/`
- `examples/cli/voicebot/`
- `examples/cli/concepts/use-project-secrets/`
- `examples/cli/concepts/use-room-secrets/`

## Snippet convention

Docs pages should not paste full YAML manifests inline.

Instead:

1. keep the manifest in `examples/cli/...`
2. create a matching wrapper snippet in `snippets/examples/cli/...`
3. import that snippet into the doc page

Small YAML fragments are still fine inline when they explain a field rather than a whole runnable manifest.
