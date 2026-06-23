import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn


class SystemSettings(BaseSettings):
    """
    Enforces strict typing and validation for environment configurations.
    Prevents black-box structural execution errors across tenant layers.
    """

    STEM_ENV: str = Field(
        default="development", description="Deployment environment flag."
    )
    DATABASE_URL: PostgresDsn = Field(..., description="PostgreSQL connection URI.")
    DB_POOL_MIN_CONNECTIONS: int = Field(
        default=1, description="Minimum pool size per tenant pipeline."
    )
    DB_POOL_MAX_CONNECTIONS: int = Field(
        default=20, description="Maximum pool capacity per tenant pipeline."
    )
    GEMINI_API_KEY: str = Field(
        ..., description="Authentication token for the Gemini orchestration layer."
    )
    MANDATORY_LATENCY_THRESHOLD_MS: int = Field(
        default=350, description="UI performance constraint."
    )

    # Looking for .env file configuration inside the parent execution layer
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Instantiate global settings block for import across all computation modules
try:
    settings = SystemSettings()
except Exception as e:
    print(
        "[CRITICAL] System configuration validation failed. Verify your environment fields."
    )
    raise e
