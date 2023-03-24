from typing import Optional
from unittest.mock import Mock

from indi import message
from indi.device import Driver, properties
from indi.device.events import Read, on
from indi.message import one_parts
from indi.routing import Router


class DummyDevice(Driver):
    name = "DEVICE"

    def __init__(
        self, side_effect, name: Optional[str] = None, router: Optional[Router] = None
    ):
        super().__init__(name, router)
        self.side_effect = side_effect

    main = properties.Group(
        "MAIN",
        vectors=dict(
            text=properties.TextVector(
                "TEXT",
                elements=dict(
                    txt=properties.Text("TXT", default="lorem"),
                ),
            ),
        ),
    )

    @on(main.text.txt, Read)
    def on_write(self, event):
        self.side_effect(event)


def test_device_emits_read_event():
    new_value = "ipsum"

    def side_effect(event):
        event.element.reset_value(new_value)

    dev = DummyDevice(side_effect)
    assert dev.main.text.txt.value == new_value
