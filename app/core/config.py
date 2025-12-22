"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys
    GEMINI_API_KEY: str
    RESEND_API_KEY: str = ""  # Opcional, pode ser vazio para modo simulação

    # Email Configuration
    EMAIL_FROM: str = "noreply@petstory.com"
    EMAIL_FROM_NAME: str = "PetStory"

    # Application
    APP_NAME: str = "PetStory API"
    DEBUG: bool = False

    # Worker Configuration
    WORKER_SLEEP_SECONDS: float = 2.0  # Delay entre gerações para evitar rate limit

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


# Singleton instance
settings = Settings()

