import os

# Memory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
GRAPH_DIR = os.path.join(DATA_DIR, "graph_image")
DB_PATH = os.path.join(DATA_DIR, "avatar_memory.db")
MCP_CONFIG_PATH = os.path.join(BASE_DIR, "mcp", "mcp_conf.json")