# Changelog

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
