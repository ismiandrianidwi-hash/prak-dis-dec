---
name: standard-idiomatic-python
description: Apply Standard's Python, application layout, startup injection, settings, route/service/lifecycle, typing, and test conventions when building or reviewing Python applications that use Standard.
license: MIT
---

# Idiomatic Python with Standard

Use this skill when creating or changing Python code in a project that uses Standard.

## Before editing

1. Run `std --version` and `std guide --format json` to identify the installed version, module map, install extras, and documentation links.
2. Read the relevant [API reference](https://appunni-m.github.io/python-standard/api/) and inspect the installed function signatures. Do not guess names or rely on undocumented internals.
3. Follow the repository's `pyproject.toml`, formatter, linter, type checker, and test commands. Keep changes within the requested scope.

## Application composition and dependency injection

Treat `main.py` as the application's composition root. It is the one place that
shows how the application is assembled and started. Construct shared
dependencies once at startup and inject them into the components that use them;
do not recreate settings, clients, or services for each request. Keep
`main.py` focused on wiring and startup, without business rules.

Use this responsibility map:

| File or layer | Responsibility |
| --- | --- |
| `main.py` | Instantiate `Settings()` once; configure logging; construct database and external clients, services, and background services; inject dependencies into routes and lifecycle management; create and start the application. |
| `core/settings.py` | Define the top-level Pydantic `Settings` aggregate and YAML-backed loading configuration. It gathers references to Pydantic models defined with their owning modules and validates/builds their nested values from YAML; it does not duplicate their fields. Only `main.py` instantiates `Settings()`. |
| `std.logging` | Configure the process logging pipeline from the composition root. Pass the application environment and service name; environment profiles select defaults and typed settings can override format, level, stream, and other options. |
| YAML configuration | Keep the single application config file and group its top-level sections by owning module. Declare environment-variable placeholders, such as `${DATABASE_URL}`, and resolve them while loading YAML through `std.config`. This is the only path from process environment into settings. |
| `lifecycle.py` | Receive already-constructed background services from `main.py` and coordinate their startup and shutdown. Keep dependency construction and business rules out of lifecycle code. |
| API routes/controllers | Stay thin: handle the transport boundary, validate or translate request/response data, call an injected service, and map expected errors to protocol responses. Do not put workflows or direct database operations here. |
| Services | Own application workflows and business rules. Receive the clients, models, and other collaborators they need through explicit constructor or function arguments. |
| Feature modules | Co-locate a feature's routes/controllers, schemas, domain or persistence models, services, repositories, and module-specific configuration in the package that owns them. Create only the files the feature needs. |
| Database models | Represent persisted data and its local constraints inside the owning feature module. Keep application workflows and orchestration in that module's services. |

Organize application code by feature (a Django-style app boundary), not by
global technical-layer folders. A change to one feature should have a clear
home. `core/` is for capabilities shared across modules, such as configuration
aggregation and service base contracts; use `std.logging` for the logging
pipeline instead of adding another app-specific formatter. It is not a second
place for feature-specific rules.

An application can use this layout as a starting point; omit packages it does
not need and keep filenames in `snake_case`:

```text
app/
├── main.py
├── lifecycle.py
├── core/
│   ├── services.py
│   └── settings.py
└── modules/
    └── billing/
        ├── api/routes.py
        ├── config.py
        ├── models.py
        ├── schemas.py
        ├── service.py
        └── repository.py
```

The example module lists common homes, not mandatory empty layers. A feature
without persistence needs no `models.py` or `repository.py`; add persistence
models and repository code beside that feature when it gains a real database
boundary. Keep API schemas distinct from persisted database models.

When using Pydantic Settings, customize its source list so direct environment
and dotenv sources do not become a second application configuration path. The
YAML source may resolve placeholders from the process environment; application
modules should not read `os.environ` or call `os.getenv` themselves.

Use Python's normal naming conventions: lowercase `snake_case.py` module and
package names, `PascalCase` classes, and `snake_case` functions and variables.
Use `test_*.py` for pytest files and mirror feature ownership in test paths when
that improves navigation, for example `tests/unit/modules/billing/`. Avoid
root-level application files that shadow standard-library imports (for example,
`logging.py`, `typing.py`, or `json.py`); namespaced modules such as
`core/logging.py` are not a conflict. Keep the dependency graph visible in
`main.py`; avoid service locators, hidden module globals, and imports that
construct dependencies as side effects.

The public `std.logging` API and its environment defaults are documented in the
API reference and [logging guide](https://appunni-m.github.io/python-standard/logging/).
Use `std.service.Service` for resources with async startup and shutdown hooks.
Use `std.service.BackgroundService` for long-running async work; its `run()`
method should observe `stop_event` and exit cleanly when shutdown is requested.
The base class exposes lifecycle state, health checks, worker failures, and a
bounded graceful-shutdown period.

## Standard core direction

Core provides configuration, `std.logging`, async `Service` lifecycle
primitives, utility helpers, the `std` CLI, and packaged agent guidance. The
FastAPI, AWS, HTTP, Redis cache, and relational database support are installed
from their matching extras or provider distributions. All six distributions
share one version derived from the release tag. Run `std guide --format json`
and consult the API reference to see the installed version's supported
modules and install paths.

## Python style

- Target the application's declared Python floor. Standard currently configures
  and tests CPython 3.11 through 3.14; do not infer support beyond that matrix.
- Prefer small functions, explicit names, standard-library types, and straightforward control flow.
- Add parameter and return annotations to public functions. Use `collections.abc` protocols for inputs when they describe the real contract.
- Use immutable values for shared configuration. Avoid mutable defaults; use `None` or a factory.
- Raise a specific exception at the boundary where invalid input is understood. Preserve useful context while keeping secrets, tokens, and raw configuration values out of errors and logs.
- Use context managers for resources and `pathlib.Path` for filesystem paths.
- Avoid broad exception handling. When an integration error must be redacted, catch at that integration boundary and emit a stable, useful public error.
- Keep optional integrations lazy or isolated. Core imports must not require an optional extra.
- Prefer correcting a lint or typing issue over suppressing it. If a narrow suppression is necessary, include its rule or mypy error code and explain the reason next to it; remove it when it is no longer needed.

## Using Standard

- Load YAML/TOML with `std.config.ConfigManager`; use its immutable `snapshot` for reads and `to_dict()` when an isolated mutable copy is needed.
- Use `reload()` only when configuration should be explicitly refreshed. A failed reload leaves the previous snapshot active.
- Use `std.collections.deep_merge` for the documented recursive mapping, list-append, and later-value-wins behavior.
- Use `std.files.atomic_write_text` when a complete text replacement must be visible atomically. Its default mode is owner-only.
- Install the published FastAPI integration with `python -m pip install 'standard[fastapi]'` before importing `std.fastapi`. From a source checkout, use `python -m pip install -e . -e packages/standard-fastapi`.
- Install the published AWS integration with `python -m pip install 'standard[aws]'` before importing `std.aws`. From a source checkout, use `python -m pip install -e . -e packages/standard-aws`. Pass a configured client when the application owns AWS client lifecycle.
- To install both integrations, use `python -m pip install 'standard[fastapi,aws]'` or, from a checkout, `python -m pip install -e . -e packages/standard-fastapi -e packages/standard-aws`.

## Tests and docs

- Add a focused regression test for each behavior change. Cover both the expected result and important failure cases.
- Prefer `tmp_path`, injected environment mappings, and fake clients over shared process state or live cloud calls.
- Use Testcontainers only for real container boundaries, and keep ordinary unit tests independent of Docker.
- Test the public API as a consumer would import it. Do not make tests depend on private helpers when a public call can prove the behavior.
- Update the relevant usage example and API reference when behavior changes.
- Run formatting, lint, types, and the narrow test set first, then the full suite.

## Agent response

State the files changed, the public behavior added or changed, and the exact checks run. Distinguish measured results from assumptions. Do not claim performance or compatibility that the executed checks do not establish.
