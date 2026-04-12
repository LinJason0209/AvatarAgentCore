
import base64
from datetime import datetime
import os
import httpx
from app.state import MESSAGE_KEY, AgentState
from app.core.system_path import GRAPH_DIR

def get_last_message(state:AgentState):
        messages = state[MESSAGE_KEY]
        return messages[-1]


async def save_graph_image(compiled_graph, output_dir: str = GRAPH_DIR):
    if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                print(f"📁 Created directory: {output_dir}")
            except Exception as e:
                return print(f"❌ Cannot create path: {output_dir}, error: {e}")
    
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S_(%A)')
    image_name = f"graph_structure_{now}.png"
    image_path = os.path.join(output_dir, image_name)
    try:
        async with httpx.AsyncClient(timeout=30.0) as client: 
            url = get_mermaid_url(compiled_graph)
            response = await client.get(url)
            
            if response.status_code == 200:
                with open(image_path, "wb") as f:
                    f.write(response.content)
                print(f"🎨 LangGraph graph save success: {image_path}")
            else:
                print(f"❌ API conversion failed (Status {response.status_code}). URL: {url}")

    except Exception as e:
        print(f"⚠️ LangGraph graph save failed: {e}")

def get_mermaid_url(compiled_graph):
     mermaid_code = compiled_graph.get_graph().draw_mermaid()
     sample_string_bytes = mermaid_code.encode("utf-8")
     base64_bytes = base64.b64encode(sample_string_bytes)
     base64_string = base64_bytes.decode("utf-8")
     return f"https://mermaid.ink/img/{base64_string}"


     