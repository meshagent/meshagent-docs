# Room Tool Search Custom Toolkit

This sample shows a room-hosted custom toolkit that a process agent can find with OpenAI Responses tool search.

The key line is in `menu_toolkit.py`: the toolkit sets `annotations={TOOL_SEARCH_ANNOTATION: "true"}`. `meshagent process join --tool-search room` only adds room toolkits with that annotation to the OpenAI tool-search candidate set.

## Try it in MeshAgent Studio

From this directory, start the custom toolkit in one terminal:

```bash
meshagent setup
meshagent rooms create tool-search-demo --if-not-exists
meshagent service run menu_toolkit.py --room tool-search-demo
```

In a second terminal, start a chat-based process agent in the same room:

```bash
meshagent process join \
  --room tool-search-demo \
  --agent-name lunch-planner \
  --channel chat \
  --model gpt-5.5 \
  --tool-search room \
  --log-llm-requests \
  --rule "You are a concise lunch-planning assistant. When a user asks about catering, menus, dietary needs, or meal budgets, use the room's searchable menu toolkit before answering."
```

Open the Studio link printed by `meshagent process join`, then send this message
to the agent in the room chat:

```text
We need lunch for 12 vegetarians tomorrow. Please recommend an option and estimate the quote with drinks.
```

If you prefer a terminal-only test, run the process agent with a toolkit channel:

```bash
meshagent process join \
  --room tool-search-demo \
  --agent-name lunch-planner \
  --channel toolkit:lunch-planner \
  --model gpt-5.5 \
  --tool-search room \
  --thread-storage none \
  --log-llm-requests \
  --rule "You are a concise lunch-planning assistant. When a user asks about catering, menus, dietary needs, or meal budgets, use the room's searchable menu toolkit before answering."
```

Then invoke the process agent from another terminal:

```bash
meshagent room agents invoke-tool \
  --room tool-search-demo \
  --toolkit lunch-planner \
  --tool run_lunch-planner_task \
  --arguments '{"prompt":"We need lunch for 12 vegetarians tomorrow. Please recommend an option and estimate the quote with drinks."}'
```

## What should happen

The menu toolkit is not passed as an always-loaded process-agent toolkit. It is registered in the room as a hosted toolkit with the `meshagent.tool_search` annotation.

With `--tool-search room`, the process agent:

1. lists room toolkits that are annotated for tool search,
2. adds those toolkits to the turn's candidate toolkit set,
3. sends OpenAI a `tool_search` tool and deferred function definitions,
4. lets the model load the matching menu tools,
5. invokes `menu-toolkit.recommend_lunch` and `menu-toolkit.calculate_catering_quote`.

With `--log-llm-requests`, the process-agent logs should show `tool_search_call`, `tool_search_output`, and then one or more `function_call` items for the menu toolkit.

You can also verify the toolkit is registered in the room:

```bash
meshagent room agents list-toolkits --room tool-search-demo
```

The output should include `menu-toolkit`, its `recommend_lunch` and
`calculate_catering_quote` tools, and the tool-search annotation:

```json
"annotations": {
  "meshagent.tool_search": "true"
}
```

If `menu-toolkit` appears with `"annotations": {}`, the toolkit is registered
and can still be called directly by name, but it is not discoverable by
`--tool-search room`.

If the process-agent logs include the OpenAI `tool_search` tool but do not show
the menu toolkit in the deferred tools, check the room `list-toolkits` response.
The room server must include toolkit annotations so the process agent can filter
for `meshagent.tool_search=true`.
