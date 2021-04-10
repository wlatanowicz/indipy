# INDIpy Quickstart Tutorial

# Server Quickstart

## 1. Install indipy

```
pip install indipy
```

## 2. Add server's main script

This is the entrypoint for your server. You have two choices:

1. Subprocess of the original indilib (http://indilib.org) (recommended)
2. Standalone INDI server

You can have both in you project and run whatever you want.

The purpose of this script is to load all the device drivers and communicate with the world or indi server.

Examples (which can be copy pasted without any changes) can be found here:
[Subprocess version](./docker-examples/server/indilib/tty.py),
[Standalone version](./docker-examples/server/standalone/server.py).

## 3. Add device driver(s) implementation

Examples above assume that device drivers are located in `devices` module. Let's create a submodule named `simple_device` with one device class `SimpleDevice` and some common imports:

```
import logging

from indi.device import Driver, non_blocking, properties
from indi.device.pool import default_pool
from indi.device.events import on, Change

logger = logging.getLogger(__name__)

@default_pool.register
class SimpleDevice(Driver):
    name = "First Simple Device"
```

In the listing above `@default_pool.register` decorator ensures that the driver is loaded automatically on startup.

INDI standard defines hierarchy of objects.
Devices are built from `groups`. Groups aggregate `vectors`. Vectors contain `elements`. Elements are the object which store values.

Let's add them to our simple device driver:

```
class SimpleDevice(Driver):
    name = "First Simple Device"

    example_group = properties.Group(
        "EXAMPLE_GROUP",
        label="Example group",
        vectors=dict(
            example_vector=properties.TextVector(
                "EXAMPLE_VECTOR",
                label="Example text vector",
                elements=dict(
                    example_element=properties.Text(
                        "EXAMPLE_ELEMENT",
                        label="Example element,
                        default="Hello INDIpy",
                    ),
                ),
            ),
        ),
    )
```

## 4. Add some logic

Whenever value is changed an `Event` object is sent. You can catch those object by implementing event handlers:

```
class SimpleDevice(Driver):
    example_group = ...

    @on(example_group.example_vector.example_element, Change)
    def text_changed(event: Change):
        logger.info(
            f"Value for example element changed from {event.old_value} to {event.new_value}"
        )
```

## 5. Ensure device driver is loaded by main script

Examples above use `*` import to load all the drivers from `devices` module:

```
from devices import *
```

In this case you need to ensure that loading `devices` module loads all individual drivers modules. It's easiest accomplished by loading all driver classes in `devices/__init__.py` file:

```
from .simple_device load SimpleDevice
```
