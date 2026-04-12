
import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage

MESSAGE_KEY = "messages"
REFLECTION_COUNT = "reflecion_count"

class AgentState(TypedDict):
    messages:Annotated[Sequence[BaseMessage], operator.add]
    critique:str
    reflecion_count:int