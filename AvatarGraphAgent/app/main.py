import argparse

from langchain_core.messages import HumanMessage
from app.graph import app_graph
from app.state import MESSAGE_KEY
from app.ui.cli import start_interactive_session

def main():
    print("--- 🤖 Local AI Agent Operation (Ollama + LangGraph) ---")

    # Simulate the user input
    # user_input = "你好，請用繁體中文簡單介紹你自己，並確認你現在使用的模型名稱。"
    # user_input = "請列出目前目錄下的檔案。"
    # user_input = "告訴我你的代號是什麼？"


    # # Set the initial config
    # initial_state = {
    #     MESSAGE_KEY:[HumanMessage(content=user_input)]
    # }

    # # Operate agent
    # result = app_graph.invoke(initial_state)
    # print("\n[AI Response]")
    # print(result[MESSAGE_KEY][-1].content)

    ControlMode()

def ControlMode():
    parser = argparse.ArgumentParser(description="AvatarAgentCore CLI")
    parser.add_argument("--mode", type=str, default="cli", choices=["cli", "api"], help="Application operation type")
    args = parser.parse_args()
    if args.mode == "cli":
        start_interactive_session()
    elif args.mode == "api":
        print("The API mode is development.")

if __name__ == "__main__":
    main()
