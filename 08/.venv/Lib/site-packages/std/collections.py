"""Small, predictable helpers for nested mappings."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from typing import Any, TypeVar

_MISSING = object()
V = TypeVar("V")


def deep_merge(*mappings: Mapping[str, Any]) -> dict[str, Any]:
    """Merge mappings without mutating inputs; lists append and later conflicts win.

    Nested mappings merge recursively. Lists concatenate in argument order.
    Any other type conflict replaces the earlier value with the later value.
    Values are copied recursively, so the result is independent of mutable inputs.
    """
    result: dict[str, Any] = {}
    for mapping in mappings:
        if not isinstance(mapping, Mapping):
            raise TypeError("deep_merge accepts mappings only")
        result = _merge_pair(result, mapping)
    return result


def _copy_value(value: Any, active: set[int] | None = None) -> Any:
    if isinstance(value, (Mapping, list, tuple)):
        current_active = active if active is not None else set()
        identity = id(value)
        if identity in current_active:
            raise ValueError("cyclic mappings and sequences cannot be merged")
        current_active.add(identity)
        try:
            if isinstance(value, Mapping):
                return {key: _copy_value(item, current_active) for key, item in value.items()}
            if isinstance(value, list):
                return [_copy_value(item, current_active) for item in value]
            return tuple(_copy_value(item, current_active) for item in value)
        finally:
            current_active.remove(identity)
    return deepcopy(value)


def _merge_pair(left: Mapping[str, Any], right: Mapping[str, Any]) -> dict[str, Any]:
    merged = {key: _copy_value(value) for key, value in left.items()}
    for key, value in right.items():
        previous = merged.get(key, _MISSING)
        if isinstance(previous, Mapping) and isinstance(value, Mapping):
            merged[key] = _merge_pair(previous, value)
        elif isinstance(previous, list) and isinstance(value, list):
            merged[key] = _copy_value(previous) + _copy_value(value)
        else:
            merged[key] = _copy_value(value)
    return merged


def get_path(
    mapping: Mapping[str, Any],
    path: str | Sequence[str],
    default: V | None = None,
) -> Any | V | None:
    """Read a dotted or segmented path from nested mappings.

    A missing segment returns ``default``. Empty path segments in a dotted path
    are ignored, so ``"a..b"`` is treated as ``("a", "b")``.
    """
    parts = (
        tuple(part for part in path.split(".") if part) if isinstance(path, str) else tuple(path)
    )
    current: Any = mapping
    for part in parts:
        if not isinstance(current, Mapping) or part not in current:
            return default
        current = current[part]
    return current


def set_path(mapping: dict[str, Any], path: str | Sequence[str], value: Any) -> None:
    """Set a nested mapping value, creating intermediate dictionaries in place."""
    parts = (
        tuple(part for part in path.split(".") if part) if isinstance(path, str) else tuple(path)
    )
    if not parts or any(not isinstance(part, str) or not part for part in parts):
        raise ValueError("path must contain at least one non-empty string segment")
    current: dict[str, Any] = mapping
    for part in parts[:-1]:
        if part not in current:
            child: Any = {}
            current[part] = child
        else:
            child = current[part]
        if not isinstance(child, dict):
            raise TypeError(f"cannot descend through non-mapping segment {part!r}")
        current = child
    current[parts[-1]] = value


__all__ = ["deep_merge", "get_path", "set_path"]
