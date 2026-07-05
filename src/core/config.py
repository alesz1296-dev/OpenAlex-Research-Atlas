"""
Configuration management for OpenAlex Research Atlas.

LEARNING NOTES:
- Environment variables are loaded from .env files
- Use pydantic-settings for validation and type safety
- Keep secrets and sensitive info in .env.local (excluded from git)
"""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    LEARNING: Pydantic BaseSettings automatically:
    - Reads from environment variables
    - Validates types (str, int, bool, etc.)
    - Provides defaults if not set
    - Raises validation errors for missing required settings
    """
    
    # Database configuration
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/openalex_research"
    DATABASE_ECHO: bool = False  # Set True to see SQL queries during development
    
    # Environment
    ENVIRONMENT: str = "development"  # development, testing, production
    DEBUG: bool = True
    
    # API configuration
    API_TITLE: str = "OpenAlex Research Atlas"
    API_VERSION: str = "0.1.0"
    API_REQUEST_ID_HEADER: str = "X-Request-ID"

    # OpenAlex ingestion configuration
    OPENALEX_BASE_URL: str = "https://api.openalex.org"
    OPENALEX_MAILTO: str | None = None
    OPENALEX_USER_AGENT: str = "OpenAlexResearchAtlas/0.1.0"
    OPENALEX_TIMEOUT_SECONDS: int = 30

    # Logging
    LOG_LEVEL: str = "INFO"

    # Azure OpenAI inference configuration.
    # Disabled by default so local tests and CI never make paid model calls.
    AZURE_OPENAI_ENABLED: bool = False
    AZURE_OPENAI_ENDPOINT: str | None = None
    AZURE_OPENAI_API_KEY: str | None = None
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    AZURE_OPENAI_CHAT_DEPLOYMENT: str | None = None
    AZURE_OPENAI_TIMEOUT_SECONDS: int = 30
    AZURE_OPENAI_MAX_RETRIES: int = 2
    AZURE_OPENAI_TEMPERATURE: float = 0.0
    AZURE_OPENAI_MAX_TOKENS: int = 800

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug_flag(cls, value):
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"release", "prod", "production"}:
                return False
        return value
    
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        case_sensitive=True,
    )


# Create global settings instance
settings = Settings()
