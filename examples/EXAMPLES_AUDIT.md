# Examples Audit

This audit focuses on the current YAML-first examples under:

- `examples/cli/`
- `examples/packaging/`

It records which docs currently import each example's snippet and recommends a target classification.

## Current CLI examples

| Current example | Current docs refs | Recommendation | Target shape |
| --- | --- | --- | --- |
| `examples/cli/analyzer/meshagent.yaml` | none | Keep, but add doc references or retire if unused | `examples/cli/analyzer/` |
| `examples/cli/chatbot/meshagent.yaml` | `cli/cli_quickstart.mdx`, `agents/standard/chatbot.mdx` | Keep | `examples/cli/chatbot/` |
| `examples/cli/codebot/meshagent.yaml` | none | Keep, but add doc references or retire if unused | `examples/cli/codebot/` |
| `examples/cli/mailbot/meshagent.yaml` | `agents/standard/mailbot.mdx` | Keep | `examples/cli/mailbot/` |
| `examples/cli/taskrunner/meshagent.yaml` | `agents/standard/taskrunner.mdx` | Keep, add README for parity | `examples/cli/taskrunner/` |
| `examples/cli/voicebot/meshagent.yaml` | `agents/standard/voicebot.mdx` | Keep | `examples/cli/voicebot/` |
| `examples/cli/worker/meshagent.yaml` | `agents/standard/worker.mdx` | Keep, add README for parity | `examples/cli/worker/` |

## Current packaging examples

| Current example | Current docs refs | Recommendation | Suggested target |
| --- | --- | --- | --- |
| `examples/packaging/anthropic_marketing.yaml` | none | Audit for doc gap or retire | `examples/cli/<scenario>/` or retire |
| `examples/packaging/anthropic_skills.yaml` | `skills/packaging_and_deploying.mdx` | Move | `examples/cli/anthropic-skills-agent/meshagent.yaml` |
| `examples/packaging/codex.yaml` | `services_room_containers/packaging_and_deploying/terminal_based_agents.mdx` | Move | `examples/cli/codex-terminal-agent/meshagent.yaml` |
| `examples/packaging/external_service.yaml` | none | Audit for doc gap or retire | `examples/cli/concepts/use-external-service/meshagent.yaml` or retire |
| `examples/packaging/mailbot.yaml` | none | Audit for duplication with `examples/cli/mailbot/` | merge or retire |
| `examples/packaging/mcp_deepwiki.yaml` | `services_room_containers/packaging_and_deploying/external_mcp_service.mdx` | Move | `examples/cli/deepwiki-mcp-service/meshagent.yaml` |
| `examples/packaging/mcp_generic_agent.yaml` | `services_room_containers/packaging_and_deploying/external_mcp_service.mdx` | Move | `examples/cli/generic-mcp-agent/meshagent.yaml` |
| `examples/packaging/mcp_supabase/mcp_supabase.yaml` | `agents/tools/supabase_mcp.mdx` | Move | `examples/cli/supabase-mcp/toolkit.yaml` |
| `examples/packaging/mcp_supabase/mcp_supabase_agent.yaml` | none | Keep with toolkit pair, add doc ref or consolidate | `examples/cli/supabase-mcp/agent.yaml` |
| `examples/packaging/meshagent_codex_writer.yaml` | none | Audit for doc gap or retire | `examples/cli/<scenario>/meshagent.yaml` or retire |
| `examples/packaging/meshagent_support.yaml` | none | Audit for doc gap or retire | `examples/cli/<scenario>/meshagent.yaml` or retire |
| `examples/packaging/meshagent_writer.yaml` | none | Audit for doc gap or retire | `examples/cli/<scenario>/meshagent.yaml` or retire |
| `examples/packaging/news_reporter.yaml` | `services_room_containers/packaging_and_deploying/multi_agent_service.mdx` | Move | `examples/cli/multi-agent-news-reporter/meshagent.yaml` |
| `examples/packaging/powerboards_chatbot_custom_rule.yaml` | `services_room_containers/share_agents_in_powerboards.mdx` | Move | `examples/cli/concepts/use-powerboards-custom-rule/meshagent.yaml` |
| `examples/packaging/process_agent_service.yaml` | `services_room_containers/packaging_and_deploying/process_agent_service.mdx` | Move | `examples/cli/process-news-agent/meshagent.yaml` |
| `examples/packaging/service_chatbot.yaml` | `services_room_containers/packaging_and_deploying/packaging.mdx` | Move as concept | `examples/cli/concepts/use-service/meshagent.yaml` |
| `examples/packaging/service_template_chatbot.yaml` | `services_room_containers/packaging_and_deploying/packaging.mdx` | Move as concept | `examples/cli/concepts/use-service-template/meshagent.yaml` |
| `examples/packaging/supabase_token.yaml` | none | Move only if still needed by Supabase docs | `examples/cli/supabase-mcp/supabase-token.yaml` or retire |

## Current gaps

- Some snippet-backed examples are not referenced by any docs page.
- Some YAML-first examples live under `packaging/` even though they are really CLI-authored service manifests.
- The current snippet system is a wrapper layer, not an automatic renderer from `examples/`.

## Secrets migration completed in this pass

New concept examples:

- `examples/cli/concepts/use-project-secrets/meshagent.yaml`
- `examples/cli/concepts/use-room-secrets/meshagent.yaml`
- `examples/cli/concepts/use-installer-secrets/meshagent.yaml`
- `examples/cli/concepts/use-image-pull-secrets/meshagent.yaml`

Matching snippet wrappers:

- `snippets/examples/cli/concepts/use-project-secrets/meshagent.mdx`
- `snippets/examples/cli/concepts/use-room-secrets/meshagent.mdx`
- `snippets/examples/cli/concepts/use-installer-secrets/meshagent.mdx`
- `snippets/examples/cli/concepts/use-image-pull-secrets/meshagent.mdx`

Docs updated to import those snippets instead of embedding full YAML inline:

- `secrets/project_secrets.mdx`
- `secrets/room_secrets.mdx`
- `secrets/image_pull_secrets.mdx`
