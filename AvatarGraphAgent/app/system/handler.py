from datetime import datetime

from langchain_core.messages import SystemMessage

from app.prompt.system_prompt import AGENT_CORE_PROMPT
from app.state import MESSAGE_KEY, AgentState

def get_system_prompt(state: AgentState, culture:str = "Location: Taipei, Taiwan"):
    history = list(state.get(MESSAGE_KEY, []))
    new_prompt = create_new_system_prompt(culture=culture)[0]["content"]

    if history and isinstance(history[0], SystemMessage):
        history[0] = SystemMessage(content=new_prompt)
    else:
        history.insert(0, SystemMessage(content=new_prompt))
    return history

def create_new_system_prompt(culture:str = "Location: Taipei, Taiwan"):
    now = datetime.now()
    env_context = (
        f"### Environment Context\n"
        f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S (%A)')}\n"
        f"{culture}\n"
        f"---------------------------\n"
    )
    system_prompt = env_context + AGENT_CORE_PROMPT
    return [{"role": "system", "content": system_prompt}]