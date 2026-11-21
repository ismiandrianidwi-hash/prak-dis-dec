"""Safe YAML/TOML loading, interpolation, merging, and atomic reloads."""

from __future__ import annotations

import json
import os
import re
import threading
import tomllib
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Final, cast

import yaml

from std.config.errors import ConfigFormatError, ConfigInterpolationError, MissingConfigSourceError
from std.config.snapshot import ConfigSnapshot

_ENV_NAME: Final = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_JSON_INVALID: Final = object()
_SAFE_YAML_LOADER: Final = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


class _NonStringYamlKeyError(Exception):
    def __init__(self, mark: Any) -> None:
        self.mark = mark


# PyYAML selects its C or Python loader at runtime, so mypy cannot resolve this base class.
class _ConfigSafeYamlLoader(_SAFE_YAML_LOADER):  # type: ignore[valid-type,misc]
    def construct_mapping(self, node: Any, deep: bool = False) -> dict[Any, Any]:
        mapping = cast(dict[Any, Any], super().construct_mapping(node, deep=deep))
        if any(not isinstance(key, str) for key in mapping):
            raise _NonStringYamlKeyError(node.start_mark)
        return mapping


class ConfigManager:
    """Load and atomically reload one or more YAML/TOML sources.

    The manager publishes immutable snapshots. A failed reload never replaces
    the last valid snapshot. ``environ=None`` reads the process environment at
    each load; a provided mapping is copied and reused until a reload override
    is passed.
    """

    def __init__(
        self,
        sources: Sequence[str | os.PathLike[str]],
        *,
        optional: bool = False,
        environ: Mapping[str, str] | None = None,
    ) -> None:
        """Load the configured sources and publish the first immutable snapshot."""
        if not sources:
            raise ValueError("at least one configuration source is required")
        self._sources = tuple(Path(source) for source in sources)
        self._optional = optional
        self._environ = dict(environ) if environ is not None else None
        self._lock = threading.RLock()
        values, source_names = self._load_values(self._environment())
        self._snapshot = ConfigSnapshot(values, revision=1, sources=source_names)

    @classmethod
    def from_file(
        cls,
        path: str | os.PathLike[str],
        *,
        optional: bool = False,
        environ: Mapping[str, str] | None = None,
    ) -> ConfigManager:
        """Create a manager for one file or directory."""
        return cls((path,), optional=optional, environ=environ)

    @classmethod
    def from_files(
        cls,
        *paths: str | os.PathLike[str],
        optional: bool = False,
        environ: Mapping[str, str] | None = None,
    ) -> ConfigManager:
        """Create a manager that composes files and directories in argument order."""
        return cls(paths, optional=optional, environ=environ)

    @property
    def snapshot(self) -> ConfigSnapshot:
        """The current immutable snapshot."""
        with self._lock:
            return self._snapshot

    def reload(self, *, environ: Mapping[str, str] | None = None) -> ConfigSnapshot:
        """Build and atomically publish a fresh snapshot, preserving the old one on error."""
        environment = dict(environ) if environ is not None else self._environment()
        values, source_names = self._load_values(environment)
        with self._lock:
            current_revision = self._snapshot.revision
            candidate = ConfigSnapshot(
                values,
                revision=current_revision + 1,
                sources=source_names,
            )
            self._snapshot = candidate
            return candidate

    def _environment(self) -> Mapping[str, str]:
        return self._environ if self._environ is not None else os.environ

    def _load_values(self, environ: Mapping[str, str]) -> tuple[dict[str, Any], tuple[str, ...]]:
        return _load_configuration(self._sources, optional=self._optional, environ=environ)


def _expand_sources(
    sources: Sequence[Path],
    *,
    optional: bool,
    allowed_extensions: frozenset[str] | None = None,
) -> tuple[Path, ...]:
    supported = allowed_extensions or frozenset({".yaml", ".yml", ".toml"})
    files: list[Path] = []
    for source in sources:
        if not source.exists():
            if optional:
                continue
            raise MissingConfigSourceError("configured source does not exist", source=source)
        if source.is_dir():
            try:
                discovered = [
                    path
                    for path in source.rglob("*")
                    if path.is_file() and path.suffix.lower() in supported
                ]
            except OSError as error:
                raise ConfigFormatError(
                    "could not inspect configuration directory", source=source
                ) from error
            files.extend(sorted(discovered, key=lambda item: item.relative_to(source).as_posix()))
            continue
        if source.suffix.lower() not in supported:
            raise ConfigFormatError(
                f"supported file extensions are {', '.join(sorted(supported))}", source=source
            )
        files.append(source)
    return tuple(files)


def _load_configuration(
    sources: Sequence[Path],
    *,
    optional: bool,
    environ: Mapping[str, str],
    allowed_extensions: frozenset[str] | None = None,
) -> tuple[dict[str, Any], tuple[str, ...]]:
    files = _expand_sources(sources, optional=optional, allowed_extensions=allowed_extensions)
    merged: dict[str, Any] = {}
    has_value = False
    for path in files:
        parsed, text = _read_file(path)
        contains_interpolation = "${" in text or "$$" in text
        contains_yaml_aliases = path.suffix.lower() != ".toml" and ("&" in text or "*" in text)
        if contains_interpolation or contains_yaml_aliases:
            resolved = _resolve_value(
                parsed,
                environ,
                path=path,
                location=[],
                stack=(),
                active=set() if contains_yaml_aliases else None,
            )
        else:
            resolved = parsed
        if not isinstance(resolved, dict):
            raise ConfigFormatError(
                "configuration root must be a mapping", source=path, location="$"
            )
        merged = _merge_config(merged, resolved) if has_value else resolved
        has_value = True
    return merged, tuple(str(path) for path in files)


def _merge_config(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    """Merge private parsed trees with copy-on-write branches."""
    merged = dict(left)
    for key, value in right.items():
        if key not in merged:
            merged[key] = value
            continue
        previous = merged[key]
        if isinstance(previous, dict) and isinstance(value, dict):
            merged[key] = _merge_config(previous, value)
        elif isinstance(previous, list) and isinstance(value, list):
            merged[key] = [*previous, *value]
        else:
            merged[key] = value
    return merged


def _read_file(path: Path) -> tuple[dict[str, Any], str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ConfigFormatError("could not read configuration source", source=path) from error
    suffix = path.suffix.lower()
    if suffix == ".toml":
        try:
            parsed = tomllib.loads(text)
        except tomllib.TOMLDecodeError as error:
            line = getattr(error, "lineno", None)
            column = getattr(error, "colno", None)
            toml_location = f"line {line}, column {column}" if line and column else None
            raise ConfigFormatError(
                "invalid TOML syntax", source=path, location=toml_location
            ) from None
    else:
        if not text.strip():
            return {}, text
        try:
            parsed = yaml.load(text, Loader=_ConfigSafeYamlLoader)
        except _NonStringYamlKeyError as error:
            mark = error.mark
            key_location = f"line {mark.line + 1}, column {mark.column + 1}"
            raise ConfigFormatError(
                "configuration keys must be strings", source=path, location=key_location
            ) from None
        except yaml.constructor.ConstructorError as error:
            if error.problem == "found unhashable key":
                mark = error.problem_mark
                unhashable_location = (
                    f"line {mark.line + 1}, column {mark.column + 1}" if mark is not None else None
                )
                raise ConfigFormatError(
                    "configuration keys must be strings", source=path, location=unhashable_location
                ) from None
            mark = getattr(error, "problem_mark", None)
            syntax_location = f"line {mark.line + 1}, column {mark.column + 1}" if mark else None
            raise ConfigFormatError(
                "invalid YAML syntax", source=path, location=syntax_location
            ) from None
        except yaml.YAMLError as error:
            mark = getattr(error, "problem_mark", None)
            syntax_location = f"line {mark.line + 1}, column {mark.column + 1}" if mark else None
            raise ConfigFormatError(
                "invalid YAML syntax", source=path, location=syntax_location
            ) from None
    if (
        parsed is None
        and suffix != ".toml"
        and all(
            not line.strip() or line.lstrip().startswith("#") or line.strip() == "---"
            for line in text.splitlines()
        )
    ):
        return {}, text
    if not isinstance(parsed, dict):
        raise ConfigFormatError("configuration root must be a mapping", source=path, location="$")
    if any(not isinstance(key, str) for key in parsed):
        raise ConfigFormatError("configuration keys must be strings", source=path, location="$")
    return parsed, text


def _resolve_value(
    value: Any,
    environ: Mapping[str, str],
    *,
    path: Path,
    location: list[str | int],
    stack: tuple[str, ...],
    active: set[int] | None,
) -> Any:
    if isinstance(value, str):
        if "$" not in value:
            return value
        return _resolve_string(value, environ, path=path, location=location, stack=stack)
    if isinstance(value, (dict, list)):
        identity: int | None = None
        if active is not None:
            identity = id(value)
            if identity in active:
                raise ConfigFormatError(
                    "cyclic YAML aliases are not supported",
                    source=path,
                    location=_format_location(location),
                )
            active.add(identity)
        try:
            if isinstance(value, dict):
                resolved_mapping: dict[str, Any] | None = None
                for key, item in value.items():
                    location.append(key)
                    try:
                        resolved_item = _resolve_value(
                            item,
                            environ,
                            path=path,
                            location=location,
                            stack=stack,
                            active=active,
                        )
                    finally:
                        location.pop()
                    if resolved_mapping is None and resolved_item is not item:
                        resolved_mapping = dict(value)
                    if resolved_mapping is not None:
                        resolved_mapping[key] = resolved_item
                return value if resolved_mapping is None else resolved_mapping

            resolved_list: list[Any] | None = None
            for index, item in enumerate(value):
                location.append(index)
                try:
                    resolved_item = _resolve_value(
                        item,
                        environ,
                        path=path,
                        location=location,
                        stack=stack,
                        active=active,
                    )
                finally:
                    location.pop()
                if resolved_list is None and resolved_item is not item:
                    resolved_list = list(value[:index])
                if resolved_list is not None:
                    resolved_list.append(resolved_item)
            return value if resolved_list is None else resolved_list
        finally:
            if active is not None and identity is not None:
                active.remove(identity)
    return value


def _resolve_string(
    text: str,
    environ: Mapping[str, str],
    *,
    path: Path,
    location: list[str | int],
    stack: tuple[str, ...],
) -> Any:
    if "$" not in text:
        return text
    if "${" not in text and "$$" not in text:
        return text

    output: list[str] = []
    index = 0
    if text.startswith("${"):
        end = _expression_end(text, 0, path, location)
        resolved = _resolve_expression_value(
            text[2:end], environ, path=path, location=location, stack=stack
        )
        if end == len(text) - 1:
            decoded = _decode_json_if_valid(resolved)
            return decoded if decoded is not _JSON_INVALID else resolved
        output.append(resolved if isinstance(resolved, str) else json.dumps(resolved))
        index = end + 1

    while index < len(text):
        dollar = text.find("$", index)
        if dollar < 0:
            output.append(text[index:])
            break
        if dollar > index:
            output.append(text[index:dollar])
        if text.startswith("$$", dollar):
            output.append("$")
            index = dollar + 2
            continue
        if text.startswith("${", dollar):
            end = _expression_end(text, dollar, path, location)
            replacement = _resolve_expression_value(
                text[dollar + 2 : end], environ, path=path, location=location, stack=stack
            )
            output.append(replacement if isinstance(replacement, str) else json.dumps(replacement))
            index = end + 1
            continue
        output.append("$")
        index = dollar + 1
    return "".join(output)


def _resolve_expression_value(
    expression: str,
    environ: Mapping[str, str],
    *,
    path: Path,
    location: list[str | int],
    stack: tuple[str, ...],
) -> Any:
    name, fallback = _split_expression(expression, path, location)
    if name in environ:
        return _resolve_environment(name, environ, path=path, location=location, stack=stack)
    if fallback is not None:
        return _resolve_string(fallback, environ, path=path, location=location, stack=stack)
    raise ConfigInterpolationError(
        f"environment variable {name} is not set",
        source=path,
        location=_format_location(location),
    )


def _format_location(location: list[str | int]) -> str:
    parts = ["$"]
    for segment in location:
        if isinstance(segment, int):
            parts.append(f"[{segment}]")
        else:
            parts.extend((".", segment))
    return "".join(parts)


def _expression_end(text: str, start: int, path: Path, location: list[str | int]) -> int:
    depth = 0
    index = start
    while index < len(text):
        if text.startswith("${", index):
            depth += 1
            index += 2
            continue
        if text[index] == "}":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    raise ConfigInterpolationError(
        "malformed interpolation placeholder",
        source=path,
        location=_format_location(location),
    )


def _split_expression(
    expression: str,
    path: Path,
    location: list[str | int],
) -> tuple[str, str | None]:
    if ":-" in expression:
        name, fallback = expression.split(":-", 1)
    else:
        name, fallback = expression, None
    if not _ENV_NAME.fullmatch(name):
        raise ConfigInterpolationError(
            "invalid environment variable name",
            source=path,
            location=_format_location(location),
        )
    return name, fallback


def _resolve_environment(
    name: str,
    environ: Mapping[str, str],
    *,
    path: Path,
    location: list[str | int],
    stack: tuple[str, ...],
) -> str:
    if name in stack:
        chain = " -> ".join((*stack, name))
        raise ConfigInterpolationError(
            f"environment interpolation cycle detected ({chain})",
            source=path,
            location=_format_location(location),
        )
    value = environ[name]
    resolved = _resolve_string(value, environ, path=path, location=location, stack=(*stack, name))
    if isinstance(resolved, str):
        return resolved
    return json.dumps(resolved)


def _decode_json_if_valid(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return _JSON_INVALID


__all__ = ["ConfigManager"]
