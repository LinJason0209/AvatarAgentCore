

from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from app.graph.edges.should_reflection_edge import ShouldRefkect
from app.graph.nodes.reflection_node import REFLECTION_NODE_NAME, ReflectionNode
from app.core.utility import save_graph_image
from app.core.env_config import config
from app.graph.nodes.agent_node import AGENT_NODE_NAME, AgentNode
from app.graph.edges.should_continue_edge import should_continue
from app.mcp.mcp_manager import mcp_manager 
from app.state import AgentState
from app.tools.file_tool import list_files, read_file_content


# Initialize the ollama connection config
llm = ChatOllama(
    model=config.LLM_MODEL,
    base_url=config.OLLAMA_BASE_URL
)

tool_list = [list_files, read_file_content]

class AvatarGraphBuilder:
    def __init__(self, base_llm, local_tools):
        self.llm:ChatOllama = base_llm
        self.local_tools = local_tools
        self.llm_with_tools = None

    def create_workflow(
            self, 
            tools, 
            agent_instance:AgentNode,
            reflection_instance:ReflectionNode,
            sould_reflection_edge:ShouldRefkect
            ):
        # Construct the Graph
        workflow = StateGraph(AgentState)

        # Add node
        workflow.add_node(AGENT_NODE_NAME, agent_instance.call_model)
        workflow.add_node("tools", ToolNode(tools))
        workflow.add_node(REFLECTION_NODE_NAME, reflection_instance.call_reflection)

        # Set entry point
        workflow.add_edge(START, AGENT_NODE_NAME)

        # set edges
        workflow.add_conditional_edges(
            AGENT_NODE_NAME, 
            should_continue,
            {
                "tools":"tools",
                "__end__":REFLECTION_NODE_NAME
                }
            )
        workflow.add_edge("tools", AGENT_NODE_NAME)
        workflow.add_conditional_edges(
            REFLECTION_NODE_NAME,
            sould_reflection_edge.should_reflect,
            {
                AGENT_NODE_NAME:AGENT_NODE_NAME,
                END:END
            }
        )
        # workflow.add_edge("agent",END)
        return workflow


    # Make the app
    async def get_async_graph(self, memory_obj:AsyncSqliteSaver):
        mcp_tools = await mcp_manager.initialize()
        all_tools = self.local_tools + mcp_tools
        self.llm_with_tools = self.llm.bind_tools(all_tools)

        agent_instance = AgentNode(self.llm_with_tools)
        reflection_instance = ReflectionNode(self.llm_with_tools)
        sould_reflection_edge = ShouldRefkect(self.llm_with_tools)

        workflow = self.create_workflow(
            all_tools, 
            agent_instance=agent_instance,
            reflection_instance=reflection_instance,
            sould_reflection_edge=sould_reflection_edge
            )
        
        compile_graph = workflow.compile(
            checkpointer=memory_obj,
            interrupt_before=[], 
            interrupt_after=[]
            )
        await save_graph_image(compile_graph)
        return compile_graph

host_graph = AvatarGraphBuilder(llm, tool_list)