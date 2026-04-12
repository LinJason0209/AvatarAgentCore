

from app.core.utility import get_last_message
from app.state import AgentState
from langchain_core.messages import HumanMessage

REFLECTION_NODE_NAME = "reflection"
REFLECTION_FINISH = "REFECTION_FINISH"
CRITIQUE = "critique"

def get_prompt(last_response):
    return [
        HumanMessage(content=f"""
                你是一位嚴格的答案審查員。請針對以下 Agent 的回答進行評估：
                ---
                {last_response}
                ---
                請檢查：
                1. 答案是否準確回答了主人的問題？
                2. 答案是否充分利用了搜尋工具提供的資訊？
                3. 格式是否清晰易讀？
                
                如果答案已經非常完美，請僅回覆「{REFLECTION_FINISH}」。
                如果答案有缺陷，請具體列出改進建議（不要直接給答案，而是給意見）。
                """)
    ]

class ReflectionNode():
    def __init__(self, model):
        self.model = model
    
    async def call_reflection(self, state:AgentState):
        last_message = get_last_message(state)
        prompt = get_prompt(last_message)
        response = await self.model.ainvoke(prompt)
        return {CRITIQUE: response.content}