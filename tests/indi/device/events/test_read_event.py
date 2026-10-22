from indi.device import Driver, properties
from indi.device.events import Read, on
from indi.routing import Router


class DummyDevice(Driver):
    name = "DEVICE"

    def __init__(self, side_effect, name: str | None = None, router: Router | None = None):
        super().__init__(name, router)
        self.side_effect = side_effect

    main = properties.Group(
        "MAIN",
        vectors={
            "text": properties.TextVector(
                "TEXT",
                elements={
                    "txt": properties.Text("TXT", default="lorem"),
                },
            ),
        },
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
