# Getting Started with MeshAgent

Welcome to the **MeshAgent Getting‑Started** sample repository!

This folder accompanies the three‑part [Getting Started with MeshAgent video series](https://www.youtube.com/playlist?list=PLxn6VUA-LspRZv5pHDzXJUrIt8ksdDujf) and contains everything you need to reproduce the demos, experiment locally, and ship your first agent.

---

## 🎬 Watch the Series

| Part                        | Topic & What you’ll learn                                                                                                                     | Video Link                                                  |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **1. Setting Up MeshAgent** | Create a free account, install the CLI, and summon your very first agent from the command line.                        | [▶ Watch Part 1](https://youtu.be/-qjQfXkg8lw) |
| **2. Building Agents**      | Evolve from a simple chat agent and voice‑enabled agent by layering on built‑in MeshAgent tools *and* a custom tool. | [▶ Watch Part 2](https://youtu.be/P1x93jRwN7s) |
| **3. Deploying an Agent**   | Package the Part 2 agents with Docker, push it to **your** container registry, and deploy the agents as a service in MeshAgent.                                   | [▶ Watch Part 3](https://youtu.be/ojnSfO_g0KQ) |

---

## 📁 Folder Structure

Below is the exact layout you’ll see after cloning the repo:

```text
getting-started/
├── agent-without-tools/          # Part 2 – Milestone 1 (chat and voice only)
│   ├── Dockerfile
│   ├── main.py
│   └── README.md
├── agent-with-meshagent-tools/   # Part 2 – Milestone 2 (add built‑in MeshAgent tools)
│   ├── Dockerfile
│   ├── main.py
│   └── README.md
├── agent-with-custom-tools/      # Part 2 – Milestone 3 (add custom tools)
│   ├── Dockerfile               # identical in every folder
│   ├── main.py
│   └── README.md
└── README.md                     # ← you are here
```

*All three agent folders share the **same `Dockerfile`**, so feel free to copy‑paste or reference it wherever needed.*

---

## ⏩ Quick Start (Part 1)

Follow the [MeshAgent Setup instructions](https://docs.meshagent.com/room_api/get_started) and [watch the video](https://youtu.be/-qjQfXkg8lw) to create your account, install MeshAgent, generate your API keys, and interact with your first agent!

Call our first chat and voice agents into a room!

```sh
meshagent process join --room YOUR_ROOM_NAME --agent-name YOUR_CHATBOT_NAME --channel chat
```

To call a voice agent into the room run: 
```sh
meshagent voicebot join --room YOUR_ROOM_NAME --agent-name YOUR_VOICEBOT_NAME --name YOUR_VOICEBOT_NAME
```

You’re now ready to dive into the full tutorials below.

---


## 🏗️ Part 2 — Building Agents

Copy the code here and follow along with the [Building an Agent in MeshAgent video](https://youtu.be/P1x93jRwN7s)!

Each folder under `getting-started/` represents a checkpoint in the tutorial series:

| Folder                        | Description                                                      |
| ----------------------------- | ---------------------------------------------------------------- |
| `agent-without-tools/`        | Minimal **chat‑only** and **voice-only** agent—your starting point.                 |
| `agent-with-meshagent-tools/` | Adds **several** built‑in MeshAgent tools. |
| `agent-with-custom-tools/`    | Introduces a **custom Python tool** you can extend or replace.   |

To run a milestone locally (assumes you have installed MeshAgent and set the required environment variables):

```bash
cd getting-started/agent-with-meshagent-tools
meshagent service run "main.py" --room=myroom
```

> **Tip:** Each milestone README walks through the new concepts introduced at that stage. You will gradually enrich main.py -- feel free to jump between folders or follow the videos step by step.

---

## 📦 Part 3 — Deploying an Agent
[Watch the video](https://youtu.be/ojnSfO_g0KQ) and follow these steps!

MeshAgent accepts any Linux/amd64 OCI image. We’ll use Docker Buildx for consistent multi‑platform builds and Zstandard compression.

> **Prerequisites:** Docker installed • Access to a container registry (Docker Hub, ACR, AWS ECR, GCP GAR, …) with **push** permissions.

### 1. One‑time builder setup

```bash
docker buildx create --name meshagent-builder --driver docker-container
docker buildx use meshagent-builder
```

### 2. Log in to *your* container registry

### 3. Build **and push** the image

```bash
docker buildx build . \
  --platform linux/amd64 \
  --output type=image,name=<registry>/<namespace>/<youragentname>:<tag>,oci-mediatypes=true,compression=zstd,compression-level=3,force-compression=true,push=true
```

> **Why Buildx?**
> - Reproducible, deterministic builds on any host OS
> - Easy multi‑arch output (ARM64, x86)
> - Zstd compression makes images \~30‑40 % smaller and uploads faster

### 4. Deploy the Agent as a Service
After the push completes, head to the [**MeshAgent Studio**](https://studio.meshagent.com), create a **New Service**, and point it at `<registry>/<namespace>/<youragentname>:<tag>`. 

You will need to save the required secrets to interact with your container registry before creating the service. 

In the Services section you will need to fill in: 
- The agent name &rarr; `chat-agent`
- The role &rarr; `agent`
- The image tag &rarr; `<registry>/<namespace>/<youragentname>:<tag>`
- The image pull secret &rarr; the secret you saved to connect to your container registry
- Port information:
    - Port number &rarr; the port you want to run the agent on
    - Service path &rarr; (this is the same path used in the code e.g. `/chat` or `/voice`)
    - Participant name &rarr; (e.g. `chat-agent`) 
    - Liveness check &rarr; (this should be `/`). *The liveness check will validate the agent is ready before deploying it into the room.*

Once the service is created it will be available in any of the rooms inside your project. To test the agent service simply enter a room and your agent will appear in the participants tab!

---

## 🛠️ Prerequisites

| Tool                   | Version | Purpose                          |
| ---------------------- | ------- | -------------------------------- |
| **Python**             | ≥ 3.13  | Run the sample agents            |
| **MeshAgent CLI**      | latest  | Interact with MeshAgent Studio and platform with ease |
| **Docker**             | ≥ 24    | Containerise & deploy (Part 3)   |
| **Container Registry** | n/a     | Where you’ll push your image     |

---

## 🙋‍♀️ Need Help?
* **Docs:** [docs.meshagent.com](https://docs.meshagent.com/)

Happy agent‑building! ✨
