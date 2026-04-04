import os
import sqlite3
from typing import Literal
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from app.mcp.mcp_manager import mcp_manager 
from app.prompt.system_prompt import AGENT_CORE_PROMPT
from app.state import MESSAGE_KEY, AgentState
from app.tools.file_tool import list_files, read_file_content

load_dotenv()

# Initialize the ollama connection config
llm = ChatOllama(
    model=os.getenv("LLM_MODEL", "gemma3:latest"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
)

tool_list = [list_files, read_file_content]

class AvatarGraphBuilder:
    def __init__(self, base_llm, local_tools):
        self.llm:ChatOllama = base_llm
        self.local_tools = local_tools
        self.llm_with_tools = None

    # Define the first note: call the model
    async def call_model(self, state:AgentState):
        history = state[MESSAGE_KEY]

        # Check and set the system prompt to be the header.
        if not any(isinstance(m, SystemMessage) for m in history):
            history = [SystemMessage(content=AGENT_CORE_PROMPT)] + history

        response = await self.llm_with_tools.ainvoke(history)
        return {MESSAGE_KEY: [response]}

    def should_continue(self, state:AgentState) -> Literal["tools", "__end__"]:
        messages = state[MESSAGE_KEY]
        last_message = messages[-1]

        if getattr(last_message, "tool_calls", None): 
            return "tools"
        return "__end__"

    def create_workflow(self, tools):
        # Construct the Graph
        workflow = StateGraph(AgentState)

        # Add node
        workflow.add_node("agent", self.call_model)
        workflow.add_node("tools", ToolNode(tools))

        # Set entry point
        workflow.add_edge(START,"agent")

        # set edges
        workflow.add_conditional_edges(
            "agent", 
            self.should_continue,
            {
                "tools":"tools",
                "__end__":END
                }
            )
        workflow.add_edge("tools", "agent")
        # workflow.add_edge("agent",END)
        return workflow


    # Make the app
    async def get_async_graph(self, memory_obj:AsyncSqliteSaver):
        mcp_tools = await mcp_manager.initialize()
        all_tools = self.local_tools + mcp_tools
        self.llm_with_tools = self.llm.bind_tools(all_tools)

        workflow = self.create_workflow(tools=all_tools)
        return workflow.compile(
            checkpointer=memory_obj,
            interrupt_before=[], 
            interrupt_after=[]
            )

app_graph = AvatarGraphBuilder(llm, tool_list)