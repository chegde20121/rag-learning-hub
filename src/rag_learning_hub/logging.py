
import logging
import logging.config
import sys
from datetime import datetime, timezone

from pythonjsonlogger.json import JsonFormatter

from rag_learning_hub.config import (
    Settings,
    LogFormat,
)


class ContextFilter(logging.Filter):
    """Add application metadata to log records."""

    def __init__(
        self,
        service: str,
        environment: str,
    ) -> None:
        super().__init__()
        self.service = service
        self.environment = environment

    def filter(self, record: logging.LogRecord) -> bool:
        record.timestamp = datetime.fromtimestamp(
            record.created,
            tz=timezone.utc,
        ).isoformat(timespec="milliseconds")

        record.service = self.service
        record.environment = self.environment

        return True


def configure_logging(settings: Settings) -> None:
    """
    Configure process-wide application logging.

    Features:
    - JSON or human-readable console output
    - UTC timestamps
    - Configurable log levels
    - Service and environment metadata
    - Structured event fields
    - Exception tracebacks
    - Safe repeated initialization
    """

    log_level = settings.log_level.value

    if settings.log_format == LogFormat.JSON:
        formatter = {
            "()": JsonFormatter,
            "fmt": (
                "%(timestamp)s %(levelname)s "
                "%(name)s %(message)s "
                "%(service)s %(environment)s"
            ),
            "rename_fields": {
                "levelname": "level",
                "name": "logger",
            },
        }
    else:
        formatter = {
            "format": (
                "%(timestamp)s | %(levelname)s | "
                "%(name)s | %(message)s | "
                "%(service)s | %(environment)s"
            ),
        }

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "context": {
                "()": ContextFilter,
                "service": settings.app_name,
                "environment": settings.environment.value,
            },
        },
        "formatters": {
            "default": formatter,
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "default",
                "filters": ["context"],
                "stream": "ext://sys.stdout",
            },
        },
        "root": {
            "level": log_level,
            "handlers": ["console"],
        },
    }

    logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)

    logger.info(
        "Logging configured",
        extra={
            "event": "logging_initialized",
            "log_level": log_level,
            "log_format": settings.log_format.value,
        },
    )
