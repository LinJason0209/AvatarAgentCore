from datetime import datetime

from langchain_core.messages import SystemMessage

from app.graph.nodes.reflection_node import CRITIQUE, REFLECTION_FINISH
from app.prompts.system.system_prompt import AGENT_CORE_PROMPT
from app.state import MESSAGE_KEY, REFLECTION_COUNT, AgentState

def get_system_prompt(state: AgentState):
    history = list(state.get(MESSAGE_KEY, []))
    new_prompt = create_new_system_prompt(state)

    if history and isinstance(history[0], SystemMessage):
        history[0] = SystemMessage(content=new_prompt)
    else:
        history.insert(0, SystemMessage(content=new_prompt))
    return history

def create_new_system_prompt(state: AgentState):
    env_context = get_env_context()
    critique_context = get_critique_context(state)

    system_prompt = env_context + critique_context + AGENT_CORE_PROMPT
    return system_prompt

def get_env_context(culture:str = "Location: Taipei, Taiwan"):
    now = datetime.now()
    return (
        f"### Environment Context\n"
        f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S (%A)')}\n"
        f"{culture}\n"
        f"---------------------------\n"
    )

def get_critique_context(state: AgentState):
    critique = state.get(CRITIQUE, "")
    reflection_count = state.get(REFLECTION_COUNT, 0)

    if critique and REFLECTION_FINISH not in critique.upper():
        reflection_instruction = f"""
        \n\n 【自我反思提醒】
        妳上一次的回答未通過審查，目前是第 {reflection_count} 次重試。
        審查員給妳的改進建議如下：
        ---
        {critique}
        ---
        請根據以上建議，結合搜尋到的工具資訊，重新整理出一份更完美、更準確的答案。
        """
        return (
            f"### Critique\n"
            f"{reflection_instruction}\n"
            f"---------------------------\n"
        )
    return ""