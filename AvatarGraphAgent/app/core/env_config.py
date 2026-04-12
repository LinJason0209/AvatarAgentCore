
from pydantic_settings import BaseSettings, SettingsConfigDict

class EnvConfig(BaseSettings):
   LLM_MODEL: str = "gemma3:latest"
   OLLAMA_BASE_URL: str = "http://host.docker.internal:11434"
   SQLITE_DB_PATH: str = "./data/memory.sqlite"
   BRAVE_API_KEY: str = ""

   model_config = SettingsConfigDict(env_file=".env", extra="ignore")

config=EnvConfig() 
