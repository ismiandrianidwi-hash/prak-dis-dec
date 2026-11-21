"""Environment-aware logging configuration built on Python's logging package."""

from __future__ import annotations

import json
import logging
import sys
from collections.abc import Mapping
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class LoggingEnvironment(StrEnum):
    """Supported environment profiles for application logging."""

    DEVELOPMENT = "development"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"

    @classmethod
    def _missing_(cls, value: object) -> LoggingEnvironment | None:
        """Accept common short environment names as aliases."""
        aliases = {
            "dev": cls.DEVELOPMENT,
            "local": cls.DEVELOPMENT,
            "stage": cls.STAGING,
            "prod": cls.PRODUCTION,
        }
        return aliases.get(value) if isinstance(value, str) else None


class LoggingLevel(StrEnum):
    """Standard Python logging severities accepted by the configuration model."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggingFormat(StrEnum):
    """Output format selected directly or from an environment profile."""

    AUTO = "auto"
    CONSOLE = "console"
    JSON = "json"
    CUSTOM = "custom"


class LoggingConfig(BaseModel):
    """Validated options for configuring the process-wide logging pipeline.

    ``auto`` uses readable console output in development and tests, and JSON
    output in staging and production. Explicit settings override those profile
    defaults. The custom format uses the format-string styles supported by
    :class:`logging.Formatter`.
    """

    model_config = ConfigDict(extra="forbid")

    level: LoggingLevel | None = None
    format: LoggingFormat = LoggingFormat.AUTO
    stream: Literal["stdout", "stderr"] = "stdout"
    color: Literal["auto", "always", "never"] = "auto"
    include_source: bool = False
    date_format: str | None = None
    custom_format: str | None = None
    custom_style: Literal["%", "{", "$"] = "%"
    logger_levels: dict[str, LoggingLevel] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_format_options(self) -> Self:
        """Reject custom-format settings that would otherwise be ignored."""
        if self.format is LoggingFormat.CUSTOM:
            if not self.custom_format:
                raise ValueError("custom_format is required when format is 'custom'")
            try:
                logging.Formatter(
                    self.custom_format,
                    datefmt=self.date_format,
                    style=self.custom_style,
                )
            except (TypeError, ValueError) as error:
                raise ValueError("custom_format is invalid for custom_style") from error
        elif self.custom_format is not None:
            raise ValueError("custom_format may only be set when format is 'custom'")

        if any(not name.strip() or name == "root" for name in self.logger_levels):
            raise ValueError("logger_levels keys must be non-empty non-root logger names")
        return self


_ENVIRONMENT_DEFAULTS: dict[LoggingEnvironment, tuple[LoggingLevel, LoggingFormat]] = {
    LoggingEnvironment.DEVELOPMENT: (LoggingLevel.DEBUG, LoggingFormat.CONSOLE),
    LoggingEnvironment.TEST: (LoggingLevel.WARNING, LoggingFormat.CONSOLE),
    LoggingEnvironment.STAGING: (LoggingLevel.INFO, LoggingFormat.JSON),
    LoggingEnvironment.PRODUCTION: (LoggingLevel.INFO, LoggingFormat.JSON),
}
_STANDARD_RECORD_FIELDS = frozenset(logging.makeLogRecord({}).__dict__) | {
    "asctime",
    "message",
}
_LEVEL_COLORS = {
    logging.DEBUG: "\x1b[36m",
    logging.INFO: "\x1b[32m",
    logging.WARNING: "\x1b[33m",
    logging.ERROR: "\x1b[31m",
    logging.CRITICAL: "\x1b[1;31m",
}
_configured_logger_names: set[str] = set()


class _UtcFormatter(logging.Formatter):
    """Formatter that renders timestamps in UTC with an ISO 8601 default."""

    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        """Render one record timestamp in UTC."""
        timestamp = datetime.fromtimestamp(record.created, tz=UTC)
        if datefmt is not None:
            return timestamp.strftime(datefmt)
        return timestamp.isoformat(timespec="milliseconds").replace("+00:00", "Z")


class _ConsoleFormatter(_UtcFormatter):
    """Readable one-line console formatter with optional terminal colors."""

    def __init__(self, *, include_source: bool, color: bool, date_format: str | None) -> None:
        source = " %(filename)s:%(lineno)d" if include_source else ""
        super().__init__(
            f"%(asctime)s %(levelname)-8s %(name)s:{source} %(message)s",
            datefmt=date_format,
        )
        self._color = color

    def format(self, record: logging.LogRecord) -> str:
        """Format the record and add severity color when enabled."""
        rendered = super().format(record)
        color = _LEVEL_COLORS.get(record.levelno)
        if not self._color or color is None:
            return rendered
        return f"{color}{rendered}\x1b[0m"


class _JsonFormatter(_UtcFormatter):
    """Render one JSON object per record, including user-supplied context."""

    def __init__(
        self,
        *,
        environment: LoggingEnvironment,
        service_name: str | None,
        include_source: bool,
    ) -> None:
        super().__init__()
        self._environment = environment.value
        self._service_name = service_name
        self._include_source = include_source

    def format(self, record: logging.LogRecord) -> str:
        """Serialize common event fields, exception details, and ``extra`` values."""
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "environment": self._environment,
        }
        if self._service_name is not None:
            payload["service"] = self._service_name
        if self._include_source:
            payload["source"] = {
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName,
            }
        if record.exc_info:
            exception_type, exception, _ = record.exc_info
            payload["exception.type"] = (
                exception_type.__name__ if exception_type is not None else "Exception"
            )
            if exception is not None:
                payload["exception.message"] = str(exception)
            payload["exception.stacktrace"] = self.formatException(record.exc_info)
        if record.stack_info:
            payload["stack_info"] = self.formatStack(record.stack_info)

        for key, value in record.__dict__.items():
            if key not in _STANDARD_RECORD_FIELDS and key not in payload:
                payload[key] = value
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), default=str)


def configure_logging(
    config: LoggingConfig | Mapping[str, object] | None = None,
    *,
    environment: LoggingEnvironment | str = LoggingEnvironment.DEVELOPMENT,
    service_name: str | None = None,
) -> None:
    """Configure root logging using an environment preset and explicit overrides.

    The defaults write to stdout so a hosting runtime can collect and route the
    event stream. Existing third-party loggers remain enabled and propagate to
    the configured root handler unless they have their own handlers.

    Args:
        config: Validated settings or a mapping accepted by ``LoggingConfig``.
            ``None`` selects all defaults for the requested environment.
        environment: One of ``development``, ``test``, ``staging``, or
            ``production``. The aliases ``dev``, ``local``, ``stage``, and
            ``prod`` are also accepted.
        service_name: Optional service identifier included in JSON records.

    Raises:
        ValueError: If ``environment`` is not supported.
        pydantic.ValidationError: If configuration values are invalid.
    """
    settings = (
        config if isinstance(config, LoggingConfig) else LoggingConfig.model_validate(config or {})
    )
    try:
        selected_environment = LoggingEnvironment(environment)
    except ValueError as error:
        supported = ", ".join(item.value for item in LoggingEnvironment)
        raise ValueError(f"unsupported logging environment; choose one of: {supported}") from error
    if service_name is not None and not service_name.strip():
        raise ValueError("service_name must not be empty when provided")

    default_level, default_format = _ENVIRONMENT_DEFAULTS[selected_environment]
    level = settings.level or default_level
    selected_format = default_format if settings.format is LoggingFormat.AUTO else settings.format
    stream = sys.stdout if settings.stream == "stdout" else sys.stderr

    if selected_format is LoggingFormat.JSON:
        formatter: logging.Formatter = _JsonFormatter(
            environment=selected_environment,
            service_name=service_name,
            include_source=settings.include_source,
        )
    elif selected_format is LoggingFormat.CUSTOM:
        formatter = _UtcFormatter(
            settings.custom_format,
            datefmt=settings.date_format,
            style=settings.custom_style,
        )
    else:
        color = settings.color == "always" or (
            settings.color == "auto"
            and selected_environment is LoggingEnvironment.DEVELOPMENT
            and stream.isatty()
        )
        formatter = _ConsoleFormatter(
            include_source=settings.include_source,
            color=color,
            date_format=settings.date_format,
        )

    handler = logging.StreamHandler(stream)
    handler.setFormatter(formatter)
    logging.basicConfig(level=level.value, handlers=[handler], force=True)

    configured_names = set(settings.logger_levels)
    for logger_name in _configured_logger_names - configured_names:
        logging.getLogger(logger_name).setLevel(logging.NOTSET)
    for logger_name, logger_level in settings.logger_levels.items():
        logging.getLogger(logger_name).setLevel(logger_level.value)
    _configured_logger_names.clear()
    _configured_logger_names.update(configured_names)


__all__ = [
    "LoggingConfig",
    "LoggingEnvironment",
    "LoggingFormat",
    "LoggingLevel",
    "configure_logging",
]
