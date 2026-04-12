

from typing import Literal
from app.core.utility import get_last_message
from app.state import AgentState

def should_continue(state:AgentState) -> Literal["tools", "__end__"]:
    # messages = state[MESSAGE_KEY]
    # last_message = messages[-1]
    last_message = get_last_message(state)

    if getattr(last_message, "tool_calls", None): 
        return "tools"
    return "__end__"