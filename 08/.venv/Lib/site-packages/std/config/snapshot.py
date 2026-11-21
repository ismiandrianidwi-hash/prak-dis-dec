"""Immutable, ready-to-read configuration snapshots."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from types import MappingProxyType
from typing import Any, TypeVar, cast

from std.collections import get_path

V = TypeVar("V")


def _freeze(value: Any, active: set[int] | None = None) -> Any:
    if isinstance(value, (Mapping, list, tuple, set)):
        current_active = active if active is not None else set()
        identity = id(value)
        if identity in current_active:
            raise ValueError("cyclic configuration values cannot be frozen")
        current_active.add(identity)
        try:
            if isinstance(value, Mapping):
                return MappingProxyType(
                    {key: _freeze(item, current_active) for key, item in value.items()}
                )
            if isinstance(value, set):
                return frozenset(_freeze(item, current_active) for item in value)
            if isinstance(value, list):
                return tuple(_freeze(item, current_active) for item in value)
            return tuple(_freeze(item, current_active) for item in value)
        finally:
            current_active.remove(identity)
    return value


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    if isinstance(value, frozenset):
        return {_thaw(item) for item in value}
    return value


class ConfigSnapshot(Mapping[str, Any]):
    """An immutable mapping produced by a configuration load or reload."""

    __slots__ = ("_values", "revision", "sources")
    _values: Mapping[str, Any]
    revision: int
    sources: tuple[str, ...]

    def __init__(
        self,
        values: Mapping[str, Any],
        *,
        revision: int = 1,
        sources: Sequence[str] = (),
    ) -> None:
        """Freeze values and attach their revision and source paths."""
        object.__setattr__(self, "_values", _freeze(values))
        object.__setattr__(self, "revision", revision)
        object.__setattr__(self, "sources", tuple(sources))

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("ConfigSnapshot is immutable")

    def __getitem__(self, key: str) -> Any:
        return self._values[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    def get_path(self, path: str | Sequence[str], default: V | None = None) -> Any | V | None:
        """Read a nested value without exposing mutable internals."""
        return get_path(self._values, path, default)

    def to_dict(self) -> dict[str, Any]:
        """Return a mutable deep copy of this snapshot."""
        return cast(dict[str, Any], _thaw(self._values))

    def __repr__(self) -> str:
        return f"ConfigSnapshot(revision={self.revision}, keys={tuple(self._values)})"


__all__ = ["ConfigSnapshot"]
