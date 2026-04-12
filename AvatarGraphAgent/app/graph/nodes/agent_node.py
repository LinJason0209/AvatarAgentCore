

from app.state import MESSAGE_KEY, REFLECTION_COUNT, AgentState
from app.prompts.system.handler import get_system_prompt

AGENT_NODE_NAME = "agent"

class AgentNode:
    def __init__(self, model):
        self.model = model

    async def call_model(self, state:AgentState):
        current_reflection_count = state.get(REFLECTION_COUNT, 0)
        response = await self.model.ainvoke(get_system_prompt(state=state))
        return {
            MESSAGE_KEY: [response],
            REFLECTION_COUNT: current_reflection_count + 1
            }
