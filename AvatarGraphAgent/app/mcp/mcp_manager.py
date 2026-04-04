import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient


class McpManager:
    def __init__(self):
        self.client = None
        self.tools = []

    async def initialize(self):
        server_config = {
            "brave-search":{
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-brave-search"],
                "env": {"BRAVE_API_KEY": "KEY"},
                "transport": "stdio"
            }
        }

        self.client = MultiServerMCPClient(server_config)
        self.tools = await self.client.get_tools()
        print(f"✅ MCP Tools Loaded: {[tool.name for tool in self.tools]}")
        return self.tools
    
    async def shutdown(self):
        try:
            if self.client:
                self.client = None 
                self.tools = []
                print("✅ MCP Resources released.")
        except Exception as e:
            print(f"⚠️ Error during MCP shutdown: {e}")

mcp_manager = McpManager()
    