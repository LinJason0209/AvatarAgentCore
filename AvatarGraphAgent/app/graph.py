import os
from typing import Literal
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

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

# Define the first note: call the model
def call_model(state:AgentState):
    history = state[MESSAGE_KEY]
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
app_graph = workflow.compile()

