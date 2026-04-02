import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph

from app.state import MESSAGE_KEY, AgentState

load_dotenv()

# Initialize the ollama connection config
llm = ChatOllama(
    model=os.getenv("LLM_MODEL", "gemma3:latest"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
)

# Define the first note: call the model
def call_model(state:AgentState):
    response = llm.invoke(state[MESSAGE_KEY])
    return {MESSAGE_KEY: [response]}

# Construct the Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

# Make the app
app_graph = workflow.compile()

