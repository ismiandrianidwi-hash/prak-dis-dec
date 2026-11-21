"""Agent-facing command line guidance for the Standard library."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path

from std import __version__
from std.files import atomic_write_text

_DISTRIBUTION_NAME = "standard"
_IMPORT_NAME = "std"
_DOCS_BASE = "https://appunni-m.github.io/python-standard/"
_SKILL_NAME = "standard-idiomatic-python"
_SKILL_INSTALL_PATH = f".agents/skills/{_SKILL_NAME}/SKILL.md"
_GUIDE = f"""Standard is installed from the `standard` distribution and imported as `std`.

Install the core package with `python -m pip install standard`. Add an extra
only for integrations you use: FastAPI uses
`python -m pip install 'standard[fastapi]'`; AWS uses
`python -m pip install 'standard[aws]'`; both use
`python -m pip install 'standard[fastapi,aws]'`. From a source checkout, use
`python -m pip install -e .` for core, and add
`-e packages/standard-fastapi` or `-e packages/standard-aws` for local
integrations. The extras are convenience selectors for the separately
published integration distributions.

Use `std.config.ConfigManager` to load YAML/TOML files, compose directories,
resolve interpolation, and read an immutable snapshot. Use `YamlSettings` or
`TomlSettings` when integrating with Pydantic Settings. `std.logging` provides
environment-aware console and JSON logging presets. Construct the app's
settings once in `main.py` and inject that instance. `std.service` provides
async lifecycle management and managed background tasks. `std.collections` and
`std.files` provide focused mapping and atomic-write helpers. `std.fastapi`
provides app setup, lifecycle, token auth, health checks, and request logging;
install its matching extra or distribution before importing it. `std.aws`
provides AWS settings and Secrets Manager support.

Start an implementation task with `std --version` and `std guide`; use
`std guide --format json` for the versioned machine-readable module and docs
map. Read the API reference before relying on an interface. The docs are at
{_DOCS_BASE}

Run `std skill show` to print the idiomatic-Python skill. Run `std skill install`
to install it at `{_SKILL_INSTALL_PATH}`; an existing file is preserved unless
you pass `--force`.
"""

_GUIDE_DATA: dict[str, object] = {
    "schema_version": 1,
    "distribution": _DISTRIBUTION_NAME,
    "import": _IMPORT_NAME,
    "command": "std",
    "version": __version__,
    "requires_python": ">=3.11",
    "install": {
        "core": "python -m pip install standard",
        "fastapi": "python -m pip install 'standard[fastapi]'",
        "aws": "python -m pip install 'standard[aws]'",
        "all_extras": "python -m pip install 'standard[fastapi,aws]'",
    },
    "modules": [
        {
            "name": "std.config",
            "availability": "core",
            "purpose": "YAML/TOML loading, Pydantic Settings sources, interpolation, and snapshots",
        },
        {
            "name": "std.collections",
            "availability": "core",
            "purpose": "nested mapping merge and path helpers",
        },
        {
            "name": "std.files",
            "availability": "core",
            "purpose": "atomic text-file replacement",
        },
        {
            "name": "std.logging",
            "availability": "core",
            "purpose": "environment-aware standard logging presets and structured JSON output",
        },
        {
            "name": "std.service",
            "availability": "core",
            "purpose": "async service lifecycle, health checks, and managed background tasks",
        },
        {
            "name": "std.fastapi",
            "availability": "extra:fastapi",
            "purpose": (
                "FastAPI application setup, lifecycle, token auth, health checks, "
                "and request logging"
            ),
        },
        {
            "name": "std.aws",
            "availability": "extra:aws",
            "purpose": "AWS Secrets Manager loader and Pydantic Settings source",
        },
    ],
    "commands": [
        "std --version",
        "std guide",
        "std guide --format json",
        "std skill show",
        "std skill path",
        "std skill install [destination] [--force]",
    ],
    "skill": {
        "name": _SKILL_NAME,
        "install_path": _SKILL_INSTALL_PATH,
        "show_command": "std skill show",
        "install_command": "std skill install",
    },
    "docs": {
        "home": _DOCS_BASE,
        "getting_started": f"{_DOCS_BASE}get-started/",
        "api_reference": f"{_DOCS_BASE}api/",
        "configuration": f"{_DOCS_BASE}configuration/",
        "logging": f"{_DOCS_BASE}logging/",
        "testing": f"{_DOCS_BASE}testing/",
        "changelog": f"{_DOCS_BASE}changelog/",
    },
    "guide": _GUIDE,
}


def _skill_resource() -> Traversable:
    return resources.files("std").joinpath("skills", _SKILL_NAME, "SKILL.md")


def _skill_text() -> str:
    return _skill_resource().read_text(encoding="utf-8")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="std",
        description="Standard library and coding-agent guidance",
    )
    parser.add_argument("--version", action="version", version=f"std {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    guide = subparsers.add_parser("guide", help="show concise instructions for coding agents")
    guide.add_argument("--format", choices=("text", "json"), default="text")

    skill = subparsers.add_parser("skill", help="show or install the idiomatic Python skill")
    skill_subparsers = skill.add_subparsers(dest="skill_command", required=True)
    skill_subparsers.add_parser("show", help="print the portable skill document")
    skill_subparsers.add_parser("path", help="print the packaged skill path when available")
    install = skill_subparsers.add_parser(
        "install", help="copy the skill into the current repository"
    )
    install.add_argument(
        "destination",
        nargs="?",
        default=_SKILL_INSTALL_PATH,
        help=f"destination file (default: {_SKILL_INSTALL_PATH})",
    )
    install.add_argument("--force", action="store_true", help="replace an existing destination")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the ``std`` command."""
    args = _parser().parse_args(argv)
    if args.command == "guide":
        if args.format == "json":
            print(json.dumps(_GUIDE_DATA, sort_keys=True))
        else:
            print(_GUIDE.rstrip())
        return 0
    if args.skill_command == "show":
        print(_skill_text(), end="")
        return 0
    if args.skill_command == "path":
        resource = _skill_resource()
        if not isinstance(resource, Path):
            print(
                "the packaged skill is not a filesystem path; use `std skill show` "
                "or `std skill install` instead",
                file=sys.stderr,
            )
            return 1
        print(resource)
        return 0
    target = Path(args.destination)
    if (target.exists() or target.is_symlink()) and not args.force:
        print(f"refusing to overwrite existing path: {target} (pass --force)", file=sys.stderr)
        return 2
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_text(target, _skill_text(), mode=0o644)
    except OSError as error:
        print(f"could not install skill at {target}: {error}", file=sys.stderr)
        return 1
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
