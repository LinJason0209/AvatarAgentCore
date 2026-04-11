import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from app.graph.nodes.agent_node import AgentNode
from app.graph.edges.chould_continue_conditional_edge import should_continue
from app.mcp.mcp_manager import mcp_manager 
from app.state import AgentState
from app.tools.file_tool import list_files, read_file_content

load_dotenv()

# Initialize the ollama connection config
llm = ChatOllama(
    model=os.getenv("LLM_MODEL", "gemma3:latest"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
)

tool_list = [list_files, read_file_content]

class AvatarGraphBuilder:
    def __init__(self, base_llm, local_tools):
        self.llm:ChatOllama = base_llm
        self.local_tools = local_tools
        self.llm_with_tools = None

    def create_workflow(self, tools, agent_instance:AgentNode):
        # Construct the Graph
        workflow = StateGraph(AgentState)

        # Add node
        workflow.add_node("agent", agent_instance.call_model)
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
        return workflow


    # Make the app
    async def get_async_graph(self, memory_obj:AsyncSqliteSaver):
        mcp_tools = await mcp_manager.initialize()
        all_tools = self.local_tools + mcp_tools
        self.llm_with_tools = self.llm.bind_tools(all_tools)
        agent_instance = AgentNode(self.llm_with_tools)

        workflow = self.create_workflow(all_tools, agent_instance)
        return workflow.compile(
            checkpointer=memory_obj,
            interrupt_before=[], 
            interrupt_after=[]
            )

host_graph = AvatarGraphBuilder(llm, tool_list)