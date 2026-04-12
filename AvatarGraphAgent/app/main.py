import argparse
import asyncio

import uvicorn
from app.ui.cli import async_start_interactive_session

def main():
    print("--- 🤖 Local AI Agent Operation (Ollama + LangGraph) ---")
    control_mode()

def control_mode():
    parser = argparse.ArgumentParser(description="AvatarAgentCore CLI")
    parser.add_argument("--mode", type=str, default="cli", choices=["cli", "api"], help="Application operation type")
    args = parser.parse_args()
    if args.mode == "cli":
        asyncio.run(async_start_interactive_session())
    elif args.mode == "api":
         uvicorn.run("app.api.v1.router:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
