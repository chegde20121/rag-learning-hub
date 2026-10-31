
import pytest
from pydantic import ValidationError

from rag_learning_hub.config import (
    Environment,
    LogFormat,
    LogLevel,
    Settings,
)


def test_default_settings(monkeypatch):
    monkeypatch.delenv("RAG_API_PORT", raising=False)

    settings = Settings(_env_file=None)

    assert settings.app_name == "rag-learning-hub"
    assert settings.environment == Environment.LOCAL
    assert settings.api_port == 8000
    assert settings.log_level == LogLevel.INFO


def test_environment_override(monkeypatch):
    monkeypatch.setenv("RAG_API_PORT", "9000")
    monkeypatch.setenv("RAG_LOG_LEVEL", "DEBUG")

    settings = Settings(_env_file=None)

    assert settings.api_port == 9000
    assert settings.log_level == LogLevel.DEBUG


def test_invalid_port(monkeypatch):
    monkeypatch.setenv("RAG_API_PORT", "70000")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_invalid_log_level(monkeypatch):
    monkeypatch.setenv("RAG_LOG_LEVEL", "VERBOSE")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_invalid_log_format(monkeypatch):
    monkeypatch.setenv("RAG_LOG_FORMAT", "xml")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_invalid_upload_limit(monkeypatch):
    monkeypatch.setenv("RAG_MAX_UPLOAD_MB", "-1")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_enum_values():
    assert Environment.PRODUCTION.value == "production"
    assert LogFormat.JSON.value == "json"