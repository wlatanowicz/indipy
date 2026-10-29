# Changelog

## Unreleased

### Features

* Add factory helpers for the remaining INDI standard properties: general devices, telescopes, CCDs and guiders, streaming, filter wheels, focusers, and domes.

### Breaking changes

* Packaging now uses `pyproject.toml` and uv. `requires-python` is `>=3.11`. black and isort are replaced by ruff.

### Fixes

* Always send `format`, `min`, `max`, and `step` on `defNumber`. Unspecified `min` and `max` are equal, which INDI treats as no range. `FocusMax` forwards `perm`, so the default read-only property is sent as `perm="ro"`.
* Build message timestamps from a timezone-aware UTC clock so `datetime.utcnow` is no longer used.
* Honor `prevent_default` on coroutine `Write` handlers. The client value is published only after each coroutine handler reaches its first await, later writes on that vector stay in order, and the read loop keeps running while the handler waits.
* Ignore client `new*Vector` messages for an unknown property or element, and keep the TTY and TCP read loops running when one client message fails.
* Serialize TTY writes so each INDI message is sent whole and in order.
* Drop a well-formed XML element that is not a valid INDI message instead of leaving it in the read buffer.
* Forward device traffic for every enableBLOB policy. Never drops setBLOBVector and still sends defBLOBVector. Also sends every message. Only sends defBLOBVector and setBLOBVector.

## 0.4.0

Goodbye threads. Welcome async.

### Features

* Dropped internal threads in favor of async coroutines.
* Event callback functions can be declared as either normal function or coroutine functions


### Breaking changes

* Removed `non_blocking` decorator.
* Both server and client entrypoint are coroutines now. The have to be run in asyncio loop ie. with `asyncio.run()`.

### Fixes

* Fixed a lot of type annotations
* Fixes in logging

## 0.3.0

Enables device cooperation while running in the same INDI server environment.

### Features

* Support for pings.
* Support for device snooping.

### Fixes

*  Ignore GetProperties message with unknown device name.
*  Fix formatting of xml messages (added declaration and trailing NL).
