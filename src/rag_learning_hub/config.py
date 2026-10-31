from enum import StrEnum
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Environment(StrEnum):
    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"

class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogFormat(StrEnum):
    JSON = "json"
    CONSOLE = "console"


class Settings(BaseSettings):
    """Deployment-time configuration for the RAG service."""

    model_config = SettingsConfigDict(
        env_prefix="RAG_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        validate_default=True,
    )

    # Application
    app_name: str = "rag-learning-hub"
    environment: Environment = Environment.LOCAL

    # Logging
    log_level: LogLevel = LogLevel.INFO
    log_format: LogFormat = LogFormat.JSON

    # API
    api_host: str = "127.0.0.1"
    api_port: int = Field(default=8000, ge=1, le=65535)

    # Ingestion
    max_upload_mb: int = Field(default=20, gt=0, le=1024)

    # PostgreSQL
    # Optional during bootstrap; required once DB integration is enabled.
    database_url: str | None = None

    # Chroma
    chroma_host: str = "localhost"
    chroma_port: int = Field(default=8001, ge=1, le=65535)
    chroma_collection: str = "rag_documents"

    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen:8b"
    ollama_timeout_seconds: int = Field(
        default=120,
        gt=0,
        le=600,
    )

    # Embeddings
    embedding_model: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    embedding_batch_size: int = Field(
        default=32,
        ge=1,
        le=512,
    )
