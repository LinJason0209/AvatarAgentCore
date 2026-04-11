import asyncio
import json
import os
import sys
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.system_path import MCP_CONFIG_PATH

MCP_ENABLE_TAG = "enabled"

class McpManager:
    def __init__(self, config_path: str = "mcp_conf.json"):
        self.config_path = config_path
        self.client = None
        self.tools = []

    async def initialize(self):
        if self.client:
            return self.tools
            
        if not os.path.exists(self.config_path):
            print(f"⚠️ Warning: {self.config_path} not found. No MCP tools loaded.")
            return []
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config_data:dict = json.load(f)
            
            # Check JSON body
            server_configs:dict = config_data.get("mcpServers", {})
            if not server_configs:
                return []
            
            # Get enable MCP
            active_config = self.get_active_config(server_configs)

            self.set_env(active_config)

            self.client = MultiServerMCPClient(active_config)
            self.tools = await self.client.get_tools()
            print(f"✅ MCP Servers Loaded: {list(active_config.keys())}")
            print(f"🛠️  Tools Available: {[tool.name for tool in self.tools]}")
            return self.tools
        
        except Exception as e:
            print(f"❌ MCP Manager Error: {e}")
            return []

    def get_active_config(self, server_configs:dict):
        active_config = {}
        for name, conf in server_configs.items():
            is_enabled = conf.get(MCP_ENABLE_TAG, True)
            if is_enabled:
                cleaned_conf = {}
                for key, value in conf.items():
                    if key != MCP_ENABLE_TAG:
                        cleaned_conf[key] = value
                active_config[name] = cleaned_conf
                print(f"✅ Enable MCP: {name}")
            else:
                print(f"🚫 Disable MCP: {name}")
        return active_config

    def set_env(self, server_configs):
        for server_id, config in server_configs.items():
            if sys.platform == "win32" and config.get("command") == "npx":
                config["command"] = "npx.cmd"

            original_env = config.get("env", {})
            combined_env = os.environ.copy()

            for k, v in original_env.items():
                if v in ("FROM_ENV", ""):
                    actual_value = os.getenv(k)
                    if not actual_value:
                        print(f"⚠️ Warning: Environment variable {k} is missing!")
                    combined_env[k] = actual_value or ""
                else:
                    combined_env[k] = v
                
            config["env"] = combined_env
            config["transport"] = "stdio"

    async def shutdown(self):
        try:
            if self.client:
                self.client = None 
                self.tools = []
                print("✅ MCP Resources released.")
        except Exception as e:
            print(f"⚠️ Error during MCP shutdown: {e}")

mcp_manager = McpManager(MCP_CONFIG_PATH)
    