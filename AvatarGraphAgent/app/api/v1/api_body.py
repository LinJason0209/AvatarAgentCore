from pydantic import BaseModel

class ChatRequest(BaseModel):
    message:str = ""
    user_id:str = "default"

HEALTH_CHECK_RESPONSE = {
    "status": "alive",
    "version": "1.0.0-alpha"
    }

class ChatResponse(BaseModel):
    thread_id: str
    message: str
