

from app.state import MESSAGE_KEY, AgentState
from app.system.handler import get_system_prompt

class AgentNode:
    def __init__(self, model):
        self.model = model

    async def call_model(self, state:AgentState):
        response = await self.model.ainvoke(get_system_prompt(state=state))
        return {MESSAGE_KEY: [response]}
