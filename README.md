# MeshAgent Documentation

This directory is the source tree for the MeshAgent docs corpus.

## What Lives Here

- Mintlify-authored MDX pages
- `docs.json` navigation and site metadata
- source-first examples under `examples/`
- generated snippet wrappers under `snippets/examples/`
- generated CLI help under `reference/meshagent_cli_help.mdx`
- public-surface metadata in `public-surfaces.yaml`

## Source Of Truth Rules

- Treat the codebase and shipped examples as the source of truth.
- Treat `examples/` as the source of truth for runnable code and YAML.
- Treat `snippets/examples/` as generated output.
- Do not hand-edit generated CLI help or generated snippets as part of normal maintenance.
- Keep archive-only material under archive paths and out of the primary learning flow.

## Main Generation Commands

From `meshagent-sdk/meshagent-docs/`:

```bash
npm run build-examples
./build-cli-help.sh
```

`build-examples` rebuilds snippet wrappers from `examples/**`.

`build-cli-help.sh` regenerates the recursive CLI reference page from the current CLI.

## Metadata

- `public-surfaces.yaml`
  Current, transitional, and archive public-surface contract for docs work.
- `examples/catalog.yaml`
  Seed catalog for canonical, archive, and non-canonical examples.

## Current Maintenance Gaps

The repo already checks snippet drift and CLI help drift in CI, but the docs system still needs:

- broader docs validation
- stronger example verification
- hygiene checks for junk and secret-like files in `examples/`
- scheduled docs audits
