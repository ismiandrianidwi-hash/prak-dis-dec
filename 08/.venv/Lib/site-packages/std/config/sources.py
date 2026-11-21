"""Pydantic Settings sources backed by Standard configuration files."""

from __future__ import annotations

import os
from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict

from std.config.loader import _load_configuration


class ConfigSettingsSource(PydanticBaseSettingsSource):
    """Read a YAML/TOML file or directory as one Pydantic Settings source."""

    def __init__(
        self,
        settings_cls: type[BaseSettings],
        *paths: str | Path,
        optional: bool = False,
        allowed_extensions: frozenset[str] | None = None,
    ) -> None:
        """Configure the Pydantic source with its paths and accepted formats."""
        super().__init__(settings_cls)
        if not paths:
            raise ValueError("at least one configuration path is required")
        self.paths = paths
        self.optional = optional
        self.allowed_extensions = allowed_extensions

    def __call__(self) -> dict[str, object]:
        """Load and return the source mapping for Pydantic Settings."""
        values, _ = _load_configuration(
            tuple(Path(path) for path in self.paths),
            optional=self.optional,
            environ=os.environ,
            allowed_extensions=self.allowed_extensions,
        )
        return values

    def get_field_value(self, field: object, field_name: str) -> tuple[object, str, bool]:
        """Satisfy the Pydantic source protocol; this source returns a full mapping."""
        return None, field_name, False


class YamlSettingsSource(ConfigSettingsSource):
    """Pydantic source restricted to YAML files and directories."""

    def __init__(
        self,
        settings_cls: type[BaseSettings],
        *paths: str | Path,
        optional: bool = False,
    ) -> None:
        """Configure a source that accepts YAML files and directories only."""
        extensions = frozenset({".yaml", ".yml"})
        super().__init__(
            settings_cls,
            *paths,
            optional=optional,
            allowed_extensions=extensions,
        )
        if any(
            Path(path).exists()
            and not Path(path).is_dir()
            and Path(path).suffix
            and Path(path).suffix.lower() not in extensions
            for path in paths
        ):
            raise ValueError("YamlSettingsSource accepts .yaml and .yml paths only")


class TomlSettingsSource(ConfigSettingsSource):
    """Pydantic source restricted to TOML files and directories."""

    def __init__(
        self,
        settings_cls: type[BaseSettings],
        *paths: str | Path,
        optional: bool = False,
    ) -> None:
        """Configure a source that accepts TOML files and directories only."""
        extensions = frozenset({".toml"})
        super().__init__(
            settings_cls,
            *paths,
            optional=optional,
            allowed_extensions=extensions,
        )
        if any(
            Path(path).exists()
            and not Path(path).is_dir()
            and Path(path).suffix
            and Path(path).suffix.lower() not in extensions
            for path in paths
        ):
            raise ValueError("TomlSettingsSource accepts .toml paths only")


class YamlSettings(BaseSettings):
    """Convenience BaseSettings class that reads ``settings.yaml`` by default."""

    model_config = SettingsConfigDict(extra="ignore")
    std_config_file: ClassVar[str | Path] = "settings.yaml"
    std_config_optional: ClassVar[bool] = False

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Keep config files above process env while preserving init precedence."""
        config_path_attribute = "std_config_file"
        optional_attribute = "std_config_optional"
        config = YamlSettingsSource(
            settings_cls,
            getattr(settings_cls, config_path_attribute),
            optional=bool(getattr(settings_cls, optional_attribute)),
        )
        return (init_settings, config, env_settings, dotenv_settings, file_secret_settings)


class TomlSettings(BaseSettings):
    """Convenience BaseSettings class that reads ``settings.toml`` by default."""

    model_config = SettingsConfigDict(extra="ignore")
    std_config_file: ClassVar[str | Path] = "settings.toml"
    std_config_optional: ClassVar[bool] = False

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Keep config files above process env while preserving init precedence."""
        config_path_attribute = "std_config_file"
        optional_attribute = "std_config_optional"
        config = TomlSettingsSource(
            settings_cls,
            getattr(settings_cls, config_path_attribute),
            optional=bool(getattr(settings_cls, optional_attribute)),
        )
        return (init_settings, config, env_settings, dotenv_settings, file_secret_settings)


__all__ = [
    "ConfigSettingsSource",
    "TomlSettings",
    "TomlSettingsSource",
    "YamlSettings",
    "YamlSettingsSource",
]
