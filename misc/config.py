# file: config.py

from dotenv import load_dotenv
load_dotenv()
from pydantic_settings import BaseSettings
from pydantic import ConfigDict 



            # ConfigDict here
class AppConfig(BaseSettings):
    """
    Centralized configuration management using Pydantic.
    Automatically reads environment variables, validates types,
    and applies default values if missing.
    """

    # API Keys
    OPENAI_API_KEY: str
    GEMINAI_API_KEY: str
    PINECONE_API_KEY: str
    LANGSMITH_API_KEY: str

    # Model config
    MODEL_PROVIDER: str = "geminai"
    DEFAULT_MODEL_NAME: str = "gemini-2.5-flash-lite"

    # LangChain tracing
    LANGSMITH_TRACING: str = "true"
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGSMITH_PROJECT: str = "cost tracking"

    # Security
    PII_DETECTION_API_URL: str = "my pie detection api"

    model_config=ConfigDict(
        # Automatically load environment variables from a .env file
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore"   ## pydantic will throw error if we have mention other Variable  other then mention here , 
    )
# Singleton instance for global access
settings = AppConfig()

# Optional: quick verification
print(f"Configuration loaded for project: {settings.LANGSMITH_API_KEY}")
print(f"Default model provider: {settings.MODEL_PROVIDER}")
