from langchain_core.messages import HumanMessage
from app.graph import app_graph
from app.state import MESSAGE_KEY

def main():
    print("--- 🤖 Local AI Agent Operation (Ollama + LangGraph) ---")

    # Simulate the user input
    user_input = "你好，請用繁體中文簡單介紹你自己，並確認你現在使用的模型名稱。"

    # Set the initial config
    initial_state = {
        MESSAGE_KEY:[HumanMessage(content=user_input)]
    }

    # Operate agent
    result = app_graph.invoke(initial_state)
    print("\n[AI Response]")
    print(result[MESSAGE_KEY][-1].content)


if __name__ == "__main__":
    main()
