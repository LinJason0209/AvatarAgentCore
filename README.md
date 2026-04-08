# AvatarAgentCore

AvatarAgentCore is a core engine for local AI avatars, providing conversation flow control and memory management capabilities through a graph-based orchestration.

## 📋 Table of Contents
- [Overview](#overview)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
- [API Usage](#api-usage)
- [Configuration](#configuration)
- [Notes & Requirements](#notes--requirements)
- [License](#license)

---

## Overview
AvatarAgentCore serves as the decision-making hub for localized virtual characters. By utilizing local LLMs and structured graph logic, it ensures low-latency responses and data privacy while maintaining persistent character states.

## Architecture & Tech Stack
- **Core Engine**: Python 3.12+ (Dependency management via `uv`)
- **API Framework**: FastAPI / Uvicorn
- **Orchestration**: LangGraph, LangChain
- **LLM Runtime**: Ollama (Local Inference)
- **Tooling**: Model Context Protocol (MCP) support
- **Persistence**: SQLite (For dialogue state and long-term memory)

## Key Features
- **Graph-Based Logic**: Deterministic and stochastic dialogue path control using LangGraph.
- **Support for Multiple Response Modes**: Seamless switching between Stream and Static API responses.
- **Privacy-First**: All inferences are performed locally via Ollama; no data is sent to external clouds.
- **Stateful Memory**: Automatic session tracking and persistence using SQLite.

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

## License
This project is licensed under the [MIT License](LICENSE).
