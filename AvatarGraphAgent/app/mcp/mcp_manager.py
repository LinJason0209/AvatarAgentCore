import json
import os
import sys
import inspect
from typing import Dict, List, Optional, Any
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.core.system_path import MCP_CONFIG_PATH

MCP_ENABLE_TAG = "enabled"

class McpManager:
    def __init__(self, config_path: str = "mcp_conf.json"):
        self.config_path: str = config_path
        self.client: Optional[MultiServerMCPClient] = None
        self.tools: List[Any] = []

    async def initialize(self) -> List[Any]:
        if self.client:
            return self.tools
            
        if not os.path.exists(self.config_path):
            print(f"⚠️ Warning: {self.config_path} not found. No MCP tools loaded.")
            return []
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config_data: dict = json.load(f)
            
            server_configs: dict = config_data.get("mcpServers", {})
            if not server_configs:
                return []
            
            active_config = self.get_active_config(server_configs)
            if not active_config:
                return []

            self.set_env(active_config)

            self.client = MultiServerMCPClient(active_config)
            self.tools = await self.client.get_tools()
            print(f"✅ MCP Servers Loaded: {list(active_config.keys())}")
            print(f"🛠️  Tools Available: {[tool.name for tool in self.tools]}")
            return self.tools
        
        except Exception as e:
            print(f"❌ MCP Manager Error: {e}")
            return []

    def get_active_config(self, server_configs: Dict[str, Any]) -> Dict[str, Any]:
        active_config: Dict[str, Any] = {}
        for name, conf in server_configs.items():
            if conf.get(MCP_ENABLE_TAG, True):
                active_config[name] = {k: v for k, v in conf.items() if k != MCP_ENABLE_TAG}
                print(f"✅ Enable MCP: {name}")
            else:
                print(f"🚫 Disable MCP: {name}")
        return active_config

    def set_env(self, server_configs: Dict[str, Any]) -> None:
        from app.core.env_config import config as env_config
        base_env = os.environ.copy()
        failed_servers = []

        for name, config in server_configs.items():
            if sys.platform == "win32" and config.get("command") == "npx":
                config["command"] = "npx.cmd"

            combined_env = base_env.copy()
            is_valid = True
            for k, v in config.get("env", {}).items():
                if v in ("FROM_ENV", ""):
                    # 完全由 env_config 統一管理環境變數
                    actual_value = getattr(env_config, k, "")
                    if not actual_value:
                        print(f"⚠️ Warning: Environment variable '{k}' is missing for MCP '{name}'! Disabling this server.")
                        is_valid = False
                        break
                    combined_env[k] = actual_value
                else:
                    combined_env[k] = str(v)
            
            if not is_valid:
                failed_servers.append(name)
                continue
                
            config["env"] = combined_env
            config["transport"] = "stdio"
            
        for name in failed_servers:
            server_configs.pop(name, None)

    async def shutdown(self) -> None:
        try:
            if self.client:
                close_func = getattr(self.client, "close", None)
                if callable(close_func):
                    close_result = close_func()
                    if inspect.isawaitable(close_result):
                        await close_result
                
            self.client = None 
            self.tools = []
            print("✅ MCP Resources released.")
        except Exception as e:
            print(f"⚠️ Error during MCP shutdown: {e}")

mcp_manager = McpManager(MCP_CONFIG_PATH)
    