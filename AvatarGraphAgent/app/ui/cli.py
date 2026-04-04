

from langchain_core.messages import HumanMessage

from app.state import MESSAGE_KEY
from app.graph import app_graph

def tidy_up_message(message):
    print(" "*60, end="\r")
    return message.content.strip()

def start_interactive_session():
    print("\n" + "="*60)
    print(" 🤖 System [Ollama + LangGraph]")
    thread_id = input("🔑 Please input thread id (<Enter> to use default):").strip() or "default"
    print(f"It is loading the chat: [{thread_id}]...")
    print("Input 'exit' or 'quit' end the app,'clear' clear the terminal window.")
    print("="*50 + "\n")
    
    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 20
    }
    
    while True:
        try:
            # Get input
            user_input = input("👤 User: ").strip()
            if not user_input: continue
            if  user_input.lower() in ["exit", "quit", "bye"]:
                print("\n👋 Agent: Disconnect")
                break
            if user_input.lower() == "clear":
                print("\033c", end="")
                continue

            # Save input to the next node 
            input_data = {MESSAGE_KEY: [HumanMessage(content=user_input)]}
            print("⏳ Agent is thinking...", end="\r")
            
            # Operate the agent
            result = app_graph.invoke(input_data, config=config)
            last_message = result[MESSAGE_KEY][-1]
            print(f"🤖 Agent Response: \n{tidy_up_message(last_message)}\n")
            print("-" * 30)

        except Exception as e:
            print(f"\n❌ Error: {e}")
            break
