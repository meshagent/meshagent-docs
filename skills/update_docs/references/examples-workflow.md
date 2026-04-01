# Code Examples Workflow

Substantial or reusable code examples in MeshAgent docs follow a pipeline: source files live in `examples/`, a build step generates importable `.mdx` snippets in `snippets/examples/`, and doc pages import those snippets.

**Do not put substantial or reusable code directly in `.mdx` files.** The exception is short inline commands or tiny illustrative snippets that are clearer in place than as imported examples.

---

## The pipeline

```
examples/                    ← you write here
    cli/my-feature/
        meshagent.yaml       ← source file
    python/snippets/
        my-feature.py        ← source file

       ↓ node build-examples.js

snippets/examples/           ← auto-generated, don't hand-edit
    cli/my-feature/
        meshagent.mdx        ← generated MDX code block
    python/snippets/
        my-feature.mdx       ← generated MDX code block

       ↓ import in .mdx doc

introduction/my-page.mdx     ← import and render
```

---

## When to use the examples pipeline

Use `examples/` plus generated snippets for:

- YAML configs
- multi-command CLI sequences
- SDK examples you may want to reuse on multiple pages
- any example that would be annoying to maintain inline

Use direct inline code in the doc page for:

- a single command
- a very short illustrative command block
- a tiny example that is tightly coupled to the surrounding explanation and unlikely to be reused

---

## Running the build

From the `meshagent-sdk/meshagent-docs/` directory:

```bash
node build-examples.js
```

This deletes and regenerates all of `snippets/examples/`. Run it after adding or editing any file in `examples/`.

---

## File extension → language mapping

The build script maps file extensions to language labels for syntax highlighting:

| Extension | Language | Tab label |
|-----------|----------|-----------|
| `.py`     | python   | Python    |
| `.sh`     | bash     | Bash      |
| `.yaml` / `.yml` | yaml | Yaml   |
| `.js`     | javascript | NodeJs  |
| `.ts`     | typescript | TypeScript |
| `.dart`   | dart     | Dart      |
| `.cs`     | dotnet   | C#        |
| `.json`   | json     | Json      |
| `Dockerfile` | dockerfile | Dockerfile |

Files with other extensions are ignored by the build.

---

## Folder conventions in `examples/`

Follow existing conventions when creating new examples:

- `examples/cli/<feature-name>/meshagent.yaml` — CLI YAML configs (ServiceTemplates, service configs)
- `examples/cli/<feature-name>/meshagent.sh` — CLI shell script sequences
- `examples/python/snippets/<name>.py` — short Python code snippets
- `examples/python/deployable/<name>/` — complete deployable Python agent examples

Look at neighboring examples to calibrate scope and style before writing a new one.

---

## Importing a snippet in a doc page

After running the build, import the generated `.mdx` file at the top of your doc page and render it with a `<CodeGroup>`:

```mdx
import MyFeatureExample from "/snippets/examples/cli/my-feature/meshagent.mdx"

...

<CodeGroup>
  <MyFeatureExample />
</CodeGroup>
```

If you have multiple language examples for the same operation, import each one and put them in the same `<CodeGroup>`:

```mdx
import MyFeatureCliExample from "/snippets/examples/cli/my-feature/meshagent.mdx"
import MyFeaturePyExample from "/snippets/examples/python/snippets/my-feature.mdx"

...

<CodeGroup>
  <MyFeatureCliExample />
  <MyFeaturePyExample />
</CodeGroup>
```

---

## Archive examples

`examples/` contains an `archive/` subdirectory with older examples using deprecated runtimes. Don't reference these in first-class docs. They exist for historical preservation only.

`snippets/examples/archive/` is the corresponding generated output. The build regenerates it, but docs should not import from it.

---

## Common mistakes to avoid

- **Editing files in `snippets/`** — they get wiped and regenerated on the next build. Always edit the source in `examples/`.
- **Putting long examples inline by default** — if the example is substantial or reusable, put it in `examples/` and import the snippet.
- **Pseudo-code in examples** — all example files should be complete and runnable.
- **Forgetting to run `build-examples.js`** — if you add a new example file, the snippet won't exist until you run the build. The doc import will silently fail or throw a build error.
