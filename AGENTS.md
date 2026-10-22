# AGENTS.md

Operating context for coding agents in this repository. Human docs stay in `README.md` and `QUICKSTART.md`.

## Product

INDIpy is a Python implementation of the INDI protocol (Instrument Neutral Distributed Interface). It provides device drivers, an in-process server, and a client.

- Import name: `indi`. PyPI name: `indipy`.
- Protocol version: `1.7` (`indi/__init__.py`, `__protocol_version__`).
- Package version: `indi/VERSION` (currently `0.4-dev`). `pyproject.toml` reads that file as the dynamic version, and `indi/__init__.py` reads it into `__version__`. `.github/workflows/release.yml` overwrites the file from the git tag before building. A leading `v` on the tag is stripped. Do not bump it by hand.
- Since 0.4 the runtime is asyncio only. Server and client entrypoints are coroutines and are started with `asyncio.run()`.

## Layout

- `indi/message/` — XML protocol messages. The class name becomes the tag (`DefTextVector` → `defTextVector`). `from_client` and `from_device` on each class decide routing. `GetProperties` is both directions.
- `indi/routing/router.py` — `Router` moves messages between `Device` and `Client`. Default BLOB policy is `Never`.
- `indi/device/` — `Driver` metaclass turns class-body `Group` definitions into getters. Runtime objects live under `properties/instance`. `@default_pool.register` plus `default_pool.init(router)` loads drivers. `@on(source, Event)` attaches handlers (plain function or coroutine). `snoop_device` requires a router.
- `indi/client/` — `BaseClient` mirrors remote devices and emits client events.
- `indi/transport/` — `Buffer` frames a TCP or TTY byte stream into XML using latin-1. TCP default port is `7624`. TTY mode is the driver subprocess controlled by indiserver.
- `docker-examples/` — runnable samples. Excluded from the installed package.
- `tests/` — pytest. Paths mirror `indi/`.

Property shape is group → vector → element. Definitions live in `indi/device/properties/definition/`; instances live in `indi/device/properties/instance/`. Switch rules, permissions, and states are in `indi/message/const.py`.

## Commands

CI in `.github/workflows/tests.yml` is the source of truth. The project manifest is `pyproject.toml`. Commit `uv.lock`. `uv sync` and `uv run` install and run tests, ruff, and mypy.

```bash
uv sync
uv run ruff check indi tests
uv run ruff format --check indi tests
uv run mypy indi
uv run pytest tests
```

`requires-python` is `>=3.11`. Ruff is pinned at `ruff==0.9.9` and checks `indi/` and `tests/`. mypy checks `indi/` only.

## Invariants

Keep these unless the task explicitly changes them:

- Message direction flags and XML tag naming (`IndiMessage.tag_name`).
- Router BLOB gating. Default policy is `Never`; blobs are forwarded only for `Also` or `Only`.
- `GetProperties` for an unknown vector name is ignored.
- Wire format from `IndiMessage.to_string`: `<?xml version="1.0"?>`, a newline, the element, and a trailing newline. Transport decoding is latin-1.
- Driver property shape: definition versus instance, group → vector → element, switch rules in `indi/message/const.py`.
- Async entrypoints. Event callbacks may be functions or coroutines. Coroutines are scheduled with `asyncio.get_running_loop().create_task`.
- Public driver and client API. 0.4 already removed threads; do not add another breaking change in passing.
- Packaging: `pyproject.toml` includes `indi*` and excludes `tests*` and `docker-examples*`. The version is dynamic from `indi/VERSION`. `MANIFEST.in` ships `indi/VERSION`.

## Tests and changelog

Add tests under `tests/indi/...` as pytest functions. Use an inline dummy `Driver` when the behavior under test is a device (see `tests/indi/device/test_device.py`). Unit tests must not require a live indiserver.

User-visible changes get a note in `CHANGELOG.md` under the current version, using the existing headings: Features, Breaking changes, Fixes.

## GitHub issues

When the task comes from a GitHub issue, fetch first, then create a fresh branch from `origin/master`. After the work is finished, open a pull request.

## Leave alone unless asked

- Do not rewrite `QUICKSTART.md` to fix typos or examples.
- Do not bump `indi/VERSION`.
- Do not restyle or reformat modules outside the change. Ruff checks `indi/` and `tests/`.
