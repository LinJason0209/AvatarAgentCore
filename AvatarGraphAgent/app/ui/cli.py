

from langchain_core.messages import HumanMessage

from app.state import MESSAGE_KEY
from app.graph import app_graph

def start_interactive_session():
    print("\n" + "="*60)
    print(" 🤖 System [Ollama + LangGraph]")
    print(" Input 'exit' or 'quit' end the app,'clear' clear the terminal window.")

    # Set the initial config
    thread_state = {
        MESSAGE_KEY:[]
        }
    
    config = {
        "recursion_limit": 10
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
            thread_state[MESSAGE_KEY].append(HumanMessage(content=user_input))
            print("⏳ Agent is thinking...", end="\r")
            
            # Operate the agent
            result = app_graph.invoke(thread_state, config=config)

            # Update histroy
            thread_state = result

            
            last_message = result[MESSAGE_KEY][-1]
            print(f"🤖 Agent Response: \n{last_message.content}\n")
            print("-" * 30)

        except KeyboardInterrupt:
            print("\n\n⚠️ Force interrupt! ")
            break
