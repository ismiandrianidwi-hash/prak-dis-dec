"""File helpers with explicit atomic-write behavior."""

from __future__ import annotations

import os
import tempfile
from contextlib import suppress
from pathlib import Path


def atomic_write_text(
    path: str | os.PathLike[str],
    text: str,
    *,
    encoding: str = "utf-8",
    mode: int = 0o600,
    create_parents: bool = False,
) -> Path:
    """Atomically replace a UTF-8 text file using a temporary sibling.

    The default file mode is owner-only. The temporary file is flushed before
    replacement, so readers see either the previous complete file or the new
    complete file. Parent directories are not created unless requested.
    """
    target = Path(path)
    if create_parents:
        target.parent.mkdir(parents=True, exist_ok=True)
    if not target.parent.is_dir():
        raise FileNotFoundError(target.parent)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding=encoding,
            newline="",
            dir=target.parent,
            prefix=f".{target.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_name = temporary.name
            temporary.write(text)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.chmod(temporary_name, mode)
        os.replace(temporary_name, target)
        temporary_name = None
        _sync_directory(target.parent)
        return target
    finally:
        if temporary_name is not None:
            with suppress(FileNotFoundError):
                os.unlink(temporary_name)


def _sync_directory(directory: Path) -> None:
    if not hasattr(os, "O_DIRECTORY"):
        return
    try:
        descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    except OSError:
        pass
    finally:
        os.close(descriptor)


__all__ = ["atomic_write_text"]
