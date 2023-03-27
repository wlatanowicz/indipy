from typing import Optional
from unittest.mock import Mock

from indi import message
from indi.device import Driver, properties
from indi.device.events import Change, on
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

    @on(main.text.txt, Change)
    def on_write(self, event):
        self.side_effect(event)


def test_device_emits_change_event_on_message():
    old_value = "lorem"
    new_value = "ipsum"
    msg = message.NewTextVector(
        device="DEVICE",
        name="TEXT",
        children=(one_parts.OneText(name="TXT", value=new_value),),
    )

    side_effect = Mock()

    dev = DummyDevice(side_effect)
    assert dev.main.text.txt.value == old_value

    dev.message_from_client(msg)

    expected_event = Change(dev.main.text.txt, old_value, new_value)
    dev.side_effect.assert_called_once_with(expected_event)

    assert dev.main.text.txt.value == new_value


def test_device_emits_change_event_on_assign():
    old_value = "lorem"
    new_value = "ipsum"

    side_effect = Mock()

    dev = DummyDevice(side_effect)
    assert dev.main.text.txt.value == old_value

    dev.main.text.txt.value = new_value

    expected_event = Change(dev.main.text.txt, old_value, new_value)
    dev.side_effect.assert_called_once_with(expected_event)

    assert dev.main.text.txt.value == new_value
