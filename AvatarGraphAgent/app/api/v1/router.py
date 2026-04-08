from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.api.v1.api_body import HEALTH_CHECK_RESPONSE, ChatRequest, ChatResponse
from app.api.v1.server import async_avatar_chat_static, async_avatar_chat_stream

router = APIRouter(
    prefix="/soulmoon/v1/stage",
    tags=["/soulmoon/v1/stage"]
)

@router.post("/chat_stream")
async def chat_stream(request:ChatRequest):
    chat_response_body = async_avatar_chat_stream(
        user_input=request.message,
        thread_id=request.user_id)
    
    return StreamingResponse(
        chat_response_body,
        media_type="text/event-stream"
    )

@router.post("/chat_static")
async def chat_static(request:ChatRequest):
    chat_message = await async_avatar_chat_static(
        user_input=request.message,
        thread_id=request.user_id
    )
    response = ChatResponse(message=chat_message, thread_id=request.user_id)
    return response

@router.get("/health")
async def health_check():
    return HEALTH_CHECK_RESPONSE

app = FastAPI(title="靈月 Avatar-1 API")
app.include_router(router)