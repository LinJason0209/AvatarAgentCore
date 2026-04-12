

from langgraph.graph import END

from app.graph.nodes.agent_node import AGENT_NODE_NAME
from app.graph.nodes.reflection_node import CRITIQUE, REFLECTION_FINISH
from app.state import REFLECTION_COUNT, AgentState

class ShouldRefkect:
    def __init__(self, max_reflection_count:int = 2):
         self.max_reflection_count= max_reflection_count
    
    def should_reflect(self, state: AgentState):
        if state.get(REFLECTION_COUNT, 0) >= self.max_reflection_count or REFLECTION_FINISH in state[CRITIQUE].upper():
            return END
        return AGENT_NODE_NAME
        