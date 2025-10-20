# file: config.py
from pydantic_settings import BaseSettings

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
    LANGCHAIN_API_KEY: str

    # Model config
    MODEL_PROVIDER: str = "geminai"
    DEFAULT_MODEL_NAME: str = "gemini-2.5-flash-lite"

    # LangChain tracing
    LANGCHAIN_TRACING_V2: str = "true"
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_PROJECT: str = "Enterprise-AI"

    # Security
    PII_DETECTION_API_URL: str = "my pie detection api"

    class Config:
        # Automatically load environment variables from a .env file
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"   ## pydantic will throw error if we have mention other Variable  other then mention here , 

# Singleton instance for global access
settings = AppConfig()

# Optional: quick verification
print(f"Configuration loaded for project: {settings.LANGCHAIN_PROJECT}")
print(f"Default model provider: {settings.MODEL_PROVIDER}")
