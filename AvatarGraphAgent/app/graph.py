import os
import sqlite3
from typing import Literal
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.sqlite import SqliteSaver

from app.prompt.system_prompt import AGENT_CORE_PROMPT
from app.state import MESSAGE_KEY, AgentState
from app.tools.file_tool import list_files, read_file_content

load_dotenv()

# Initialize the ollama connection config
llm = ChatOllama(
    model=os.getenv("LLM_MODEL", "gemma3:latest"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
)
tools = [list_files, read_file_content]
llm_with_tools = llm.bind_tools(tools)

# Memory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "avatar_memory.db")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
    print(f"📁 Create the Data directory: {DATA_DIR}")

memory_connect = sqlite3.connect(DB_PATH, check_same_thread=False)
memory = SqliteSaver(memory_connect)

# Define the first note: call the model
def call_model(state:AgentState):
    history = state[MESSAGE_KEY]

    # Check and set the system prompt to be the header.
    if not any(isinstance(m, SystemMessage) for m in history):
        history = [SystemMessage(content=AGENT_CORE_PROMPT)] + history

    response = llm_with_tools.invoke(history)
    return {MESSAGE_KEY: [response]}

def should_continue(state:AgentState) -> Literal["tools", "__end__"]:
    messages = state[MESSAGE_KEY]
    last_message = messages[-1]

    if getattr(last_message, "tool_calls", None): 
        return "tools"
    return "__end__"

# Construct the Graph
workflow = StateGraph(AgentState)

# Add node
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

# Set entry point
workflow.add_edge(START,"agent")

# set edges
workflow.add_conditional_edges(
    "agent", 
    should_continue,
    {
        "tools":"tools",
        "__end__":END
        }
    )
workflow.add_edge("tools", "agent")
# workflow.add_edge("agent",END)

# Make the app
app_graph = workflow.compile(
    checkpointer=memory,
    interrupt_before=[], 
    interrupt_after=[]
    )

