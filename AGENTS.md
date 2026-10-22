# AGENTS.md

Operating context for coding agents in this repository. Human docs stay in `README.md` and `QUICKSTART.md`.

## Product

INDIpy is a Python implementation of the INDI protocol (Instrument Neutral Distributed Interface). It provides device drivers, an in-process server, and a client.

- Import name: `indi`. PyPI name: `indipy`.
- Protocol version: `1.7` (`indi/__init__.py`, `__protocol_version__`).
- Package version: `indi/VERSION` (currently `0.4-dev`). `.github/workflows/release.yml` overwrites that file from the git tag on publish. Do not bump it by hand.
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

CI in `.github/workflows/tests.yml` is the source of truth. The project manifest is `setup.py` plus `requirements/`. Keep that layout.

```bash
pip install -r requirements/tests.txt
pip install -r requirements/types.txt
pip install -r requirements/lint.txt
python -m black --check indi
python -m isort --profile black indi
python -m mypy indi
python -m pytest tests
```

Pins in `requirements/lint.txt`: `black==22.3.0`, `isort==5.11.5`, `mypy==1.1.1`. Black, isort, and mypy cover `indi/` only. `python_requires` and CI still include Python 3.7. `tox.ini` installs a non-existent extra `.[d]`; do not treat tox as the check command.

## Invariants

Keep these unless the task explicitly changes them:

- Message direction flags and XML tag naming (`IndiMessage.tag_name`).
- Router BLOB gating. Default policy is `Never`; blobs are forwarded only for `Also` or `Only`.
- `GetProperties` for an unknown vector name is ignored.
- Wire format from `IndiMessage.to_string`: `<?xml version="1.0"?>`, a newline, the element, and a trailing newline. Transport decoding is latin-1.
- Driver property shape: definition versus instance, group → vector → element, switch rules in `indi/message/const.py`.
- Async entrypoints. Event callbacks may be functions or coroutines. Coroutines are scheduled with `asyncio.get_running_loop().create_task`.
- Public driver and client API. 0.4 already removed threads; do not add another breaking change in passing.
- Packaging: `find_packages` excludes `tests*` and `docker-examples`. `MANIFEST.in` ships `indi/VERSION` and `requirements/*.txt`.

## Tests and changelog

Add tests under `tests/indi/...` as pytest functions. Use an inline dummy `Driver` when the behavior under test is a device (see `tests/indi/device/test_device.py`). Unit tests must not require a live indiserver.

User-visible changes get a note in `CHANGELOG.md` under the current version, using the existing headings: Features, Breaking changes, Fixes.

## Leave alone unless asked

- Do not rewrite `QUICKSTART.md` to fix typos or examples.
- Do not migrate packaging to `pyproject.toml` or uv.
- Do not bump `indi/VERSION`.
- Do not restyle or reformat modules outside the change. Formatters apply to `indi/` only, with the pinned tool versions above.
