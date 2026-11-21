"""Public errors raised while loading and resolving configuration."""

from __future__ import annotations

from pathlib import Path


class ConfigError(Exception):
    """Base error with optional source and location context."""

    def __init__(
        self,
        message: str,
        *,
        source: Path | None = None,
        location: str | None = None,
    ) -> None:
        """Build a safe error message with optional source and location context."""
        self.message = message
        self.source = source
        self.location = location
        context = []
        if source is not None:
            context.append(str(source))
        if location:
            context.append(location)
        prefix = ":".join(context)
        super().__init__(f"{prefix}: {message}" if prefix else message)


class MissingConfigSourceError(ConfigError):
    """A required configuration file or directory is missing."""


class ConfigFormatError(ConfigError):
    """A source has invalid syntax, a bad root, or an unsupported format."""


class ConfigInterpolationError(ConfigError):
    """A placeholder is malformed or cannot be resolved safely."""
