# MeshAgent Quickstarts

Try **chat**, **voice**, **developer**, **analyzer**, and **mail** agents in minutes. These quickstarts use the MeshAgent CLI so you can experiment without writing code. The CLI lets you call agents into a room for testing, easily add tools to agents, deploy services, and more.

## What each quickstart includess
- **`meshagent.yaml`** — a Service (or ServiceTemplate) for deploying the agent in MeshAgent Studio using a maintained public image.
- **`README.md`** — step-by-step instructions for:
  - **Running locally** with the MeshAgent CLI (quickest path)
  - **Deploying as a service** in MeshAgent Studio (always-on)

Language-specific examples (e.g., `python/`) provide source-level variants if you want to modify agent code instead of using CLI entrypoints.

## Available quickstarts

- **Chatbot** — text chat with optional web search, image generation, and room storage.
- **VoiceBot** — voice in/out in Studio with the same optional tools.
- **Analyzer** — analyzes documents and has local shell tools.
- **Developer (Codebot)** — coding & shell workflows with room storage and web tools.
- **Mail** — email-style flows (where supported).

## Pre-built container images

Browse the latest public images here: us-central1-docker.pkg.dev/meshagent-public/images

(Each quickstart’s meshagent.yaml references a public CLI image you can use as-is.)

## Prerequisites
- MeshAgent account — sign up at [studio.meshagent.com](https://studio.meshagent.com)
- MeshAgent CLI installed (e.g., uv add "meshagent[all]")

---
## For more information see: 

**Website**: www.meshagent.com(https://www.meshagent.com)
**Documentation**: docs.meshagent.com(https://docs.meshagent.com/)
