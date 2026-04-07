
import os

from langchain_core.messages import HumanMessage

from app.state import MESSAGE_KEY
from app.system_path import DATA_DIR, DB_PATH


def get_config_dic(thread_id):
    return{
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 20
    }

def get_human_message(user_input:str):
    return  {MESSAGE_KEY: [HumanMessage(content=user_input)]}

def get_db_path():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"📁 Create the Data directory: {DATA_DIR}")
    return DB_PATH