# AvatarAgentCore

AvatarAgentCore is a dialogue control engine for local AI avatars. It uses **LangGraph** to manage conversation flows and **Ollama** for local model inference, supporting tool integration and session persistence.

---

## 🛠 Tech Stack

- **Orchestration**: LangGraph
- **LLM Inference**: Ollama
- **Tool Protocol**: Model Context Protocol (MCP)
- **API Framework**: FastAPI
- **Persistence**: SQLite (Checkpointer)
- **Dependency Management**: uv

---

## Core Features

### 1. LangGraph Workflow
The dialogue process is built on a directed graph that includes:
- **Agent Reasoning**: Running the LLM to process input and decide on actions.
- **Tool Execution**: Calling local functions or remote MCP tools.
- **Self-Reflection**: Re-evaluating model outputs for better response quality.
- **Conditional Paths**: Using logic to decide whether to call tools, reflect, or end the chat.

### 2. MCP Tool Integration
Supports loading tools from external MCP servers. These tools are combined with local functions and bound to the LLM to expand its capabilities.

### 3. Session Persistence
Uses SQLite to save the state of each conversation thread. This allows the system to remember chat history across restarts based on a session ID.

### 4. API Interface
- **Streaming**: Real-time message output using Server-Sent Events (SSE).
- **Static**: Typical HTTP response that returns the full message after all processing is done.

---

## 📂 Project Structure

```text
AvatarGraphAgent/
├── app/
│   ├── api/            # API routes and server setup
│   ├── core/           # Configuration and environment settings
│   ├── graph/          # LangGraph nodes and workflow implementation
│   ├── mcp/            # MCP client and tool management
│   ├── memory/         # TODO
│   └── tools/          # Local tool definitions
├── data/               # SQLite files and runtime data
├── mcp_conf.json       # MCP server configuration
├── pyproject.toml      # Dependency file
└── .env                # Environment variables
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.12+**
- **Ollama** installed and running

## Getting Started

### Prerequisites
1. **Python 3.12+** environment.
2. **Ollama** installed and running with your preferred models.
3. Configure environment variables in `.env` (refer to `.env.sample`).

### Installation & Execution
Navigate to the `AvatarGraphAgent` directory and choose one of the following methods:

#### Method A: Local Python Environment
```bash
cd AvatarGraphAgent
uvicorn app.api.v1.router:app --reload --port 8000
```

#### Method B: Docker (Recommended for Deployment)
```bash
cd AvatarGraphAgent
docker-compose up -d
```
The service will be accessible at `http://localhost:8000`.

## API Usage

### Stream Response (POST `/v1/stage/chat_stream`)
```bash
curl -X POST "http://127.0.0.1:8000/soulmoon/v1/stage/chat_stream" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello! Introduce yourself.", "user_id": "test_user"}'
```

### Static Response (POST `/v1/stage/chat_static`)
```bash
curl -X POST "http://127.0.0.1:8000/soulmoon/v1/stage/chat_static" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello! Introduce yourself.", "user_id": "test_user"}'
```

## Configuration

### Ollama Connectivity for Docker
To enable the Docker container to access Ollama on the host machine via `http://host.docker.internal:11434`, you must configure Ollama to listen on all interfaces:

- **Windows**:
  1. Add System Environment Variable `OLLAMA_HOST` with value `0.0.0.0`.
  2. Restart Ollama from the system tray.
- **Linux / macOS**:
  1. Export the variable: `export OLLAMA_HOST="0.0.0.0"`.
  2. Restart the Ollama service.

---

## Hardware Environment (Reference)
This project was developed and tested on the following hardware configuration:
- **CPU**: Intel(R) Core(TM) i7-10700F @ 2.90GHz
- **GPU**: NVIDIA GeForce RTX 3060 (12GB VRAM)
- **RAM**: 32GB DDR4
- **OS**: Windows 10 (with Docker Desktop & WSL2 support)

## Notes & Requirements

- **Performance**: Inference speed depends on host hardware (GPU VRAM/System RAM).
- **Persistence**: Data is stored in the `data/` directory. In Docker, this is managed via a persistent volume.

---

## 📡 API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/v1/stage/chat_stream` | `POST` | Real-time SSE stream |
| `/v1/stage/chat_static` | `POST` | Full static response |

---

## ⚖ License
MIT License
