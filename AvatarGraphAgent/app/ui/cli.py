
import os

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langchain_core.messages import AIMessageChunk, HumanMessage

from app.state import MESSAGE_KEY
from app.graph import get_async_graph
from app.system_path import DATA_DIR, DB_PATH

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

def get_config_dic(thread_id):
    return{
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 20
    }

async def async_interactive_session(user_input, config, app_graph):
    input_data = {MESSAGE_KEY: [HumanMessage(content=user_input)]}
    print("⏳ Agent is thinking...", end="\r")

    full_response = ""
    first_chunk = True

    async for message, metadata in app_graph.astream(
        input=input_data,
        config=config,
        stream_mode="messages"):
        if isinstance(message, AIMessageChunk) and message.content:
            if first_chunk:
                tidy_up_message()
                print(f"🤖 Agent Response: ", end="", flush=True)
                first_chunk = False

            print(message.content, end="", flush=True)
            full_response += message.content
    print("\n" + "-" * 30)
    
async def async_session_loop(app_graph, config):
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
                    app_graph=app_graph
                )

            except Exception as e:
                print(f"\n❌ Error: {e}")
                break

async def async_start_interactive_session():
    thread_id = get_thread_id()
    config = get_config_dic(thread_id)
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"📁 Create the Data directory: {DATA_DIR}")

    async with AsyncSqliteSaver.from_conn_string(DB_PATH) as memory:
        app_graph = get_async_graph(memory_obj=memory)
        await async_session_loop(app_graph=app_graph, config=config)

        
