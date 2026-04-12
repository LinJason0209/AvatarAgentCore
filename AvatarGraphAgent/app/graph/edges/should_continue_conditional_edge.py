

from typing import Literal
from app.state import MESSAGE_KEY, AgentState


def should_continue(state:AgentState) -> Literal["tools", "__end__"]:
    messages = state[MESSAGE_KEY]
    last_message = messages[-1]

    if getattr(last_message, "tool_calls", None): 
        return "tools"
    return "__end__"