
import os

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langchain_core.messages import AIMessageChunk

from app.chat import get_config_dic, get_db_path, get_human_message
from app.graph.builder.host_builder import host_graph

def tidy_up_message(message = ""):
    print(" "*60, end="\r")
    if message:
        return message.content.strip()
    return ""

def get_thread_id():
    print("\n" + "="*60)
    print(" 🤖 System [Ollama + LangGraph]")
    thread_id = input("🔑 Please input thread id (<Enter> to use default):").strip() or "default"
    print(f"It is loading the chat: [{thread_id}]...")
    print("Input 'exit' or 'quit' end the app,'clear' clear the terminal window.")
    print("="*50 + "\n")
    return thread_id


async def async_interactive_session(user_input, config, app_graph):
    input_data = get_human_message(user_input)
    print("⏳ Agent is thinking...", end="\r")

    full_response = ""
    first_chunk = True

    async for message, metadata in app_graph.astream(
        input=input_data,
        config=config,
        stream_mode="messages"):
        if metadata.get("langgraph_node") == "agent" and isinstance(message, AIMessageChunk) and message.content:
            if first_chunk:
                tidy_up_message()
                print(f"🤖 Agent Response: ", end="", flush=True)
                first_chunk = False

            print(message.content, end="", flush=True)
            full_response += message.content
    print("\n" + "-" * 30)
    
async def async_session_loop(graph, config):
    while True:
            try:
                # Get input
                user_input = input("👤 User: ").strip()
                if not user_input: continue
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("\n👋 Agent: Disconnect")
                    break
                if user_input.lower() == "clear":
                    print("\033c", end="")
                    continue
                
                await async_interactive_session(
                    user_input=user_input,
                    config=config,
                    app_graph=graph
                )

            except Exception as e:
                print(f"\n❌ Error: {e}")
                break

async def async_start_interactive_session():
    from app.mcp.mcp_manager import mcp_manager
    thread_id = get_thread_id()
    config = get_config_dic(thread_id)
    db_path = get_db_path()

    try:
        async with AsyncSqliteSaver.from_conn_string(db_path) as memory:
            compiled_graph = await host_graph.get_async_graph(memory_obj=memory)
            await async_session_loop(graph=compiled_graph, config=config)
    finally:
        await mcp_manager.shutdown()

        
