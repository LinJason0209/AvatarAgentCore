import json

from langchain_core.messages import AIMessageChunk
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from app.api.v1.api_body import ChatResponse
from app.chat import get_config_dic, get_db_path, get_human_message
from app.graph.builder.host_builder import host_graph

async def async_avatar_chat_stream(user_input:str, thread_id:str):
    config = get_config_dic(thread_id)
    input_data = get_human_message(user_input)
    db_path = get_db_path()

    async with AsyncSqliteSaver.from_conn_string(db_path) as memory:
        compiled_graph = await host_graph.get_async_graph(memory_obj=memory)
        async for message, metadata in compiled_graph.astream(
                input=input_data,
                config=config,
                stream_mode="messages"):
            if metadata.get("langgraph_node") == "agent" and isinstance(message, AIMessageChunk) and message.content:
                response = ChatResponse(message=message.content, thread_id=thread_id)
                yield f"data: {response.model_dump_json()}\n\n"

async def async_avatar_chat_static(user_input:str, thread_id:str):
    full_response = ""
    async for chunk in async_avatar_chat_stream(user_input, thread_id):
        raw_json = chunk.replace("data: ", "").strip()
        if raw_json:
            data = json.loads(raw_json)
            full_response += data["message"]
    return full_response
    
            
            