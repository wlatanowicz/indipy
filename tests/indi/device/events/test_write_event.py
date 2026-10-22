import asyncio
from unittest.mock import Mock

from indi import message
from indi.device import Driver, properties
from indi.device.events import Write, on
from indi.message import one_parts
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

    @on(main.text.txt, Write)
    def on_write(self, event):
        self.side_effect(event)


def test_device_emits_write_event():
    new_value = "ipsum"
    msg = message.NewTextVector(
        device="DEVICE",
        name="TEXT",
        children=(one_parts.OneText(name="TXT", value=new_value),),
    )

    side_effect = Mock()

    dev = DummyDevice(side_effect)
    assert dev.main.text.txt.value == "lorem"

    dev.message_from_client(msg)

    expected_event = Write(dev.main.text.txt, new_value)
    dev.side_effect.assert_called_once_with(expected_event)

    assert dev.main.text.txt.value == new_value


def test_device_write_event_prevent_default():
    new_value = "ipsum"
    msg = message.NewTextVector(
        device="DEVICE",
        name="TEXT",
        children=(one_parts.OneText(name="TXT", value=new_value),),
    )

    def side_effect(event):
        event.prevent_default = True

    dev = DummyDevice(side_effect)
    assert dev.main.text.txt.value == "lorem"

    dev.message_from_client(msg)

    assert dev.main.text.txt.value == "lorem"
    assert dev.main.text.txt.value != new_value


def _new_text(value: str) -> message.NewTextVector:
    return message.NewTextVector(
        device="DEVICE",
        name="TEXT",
        children=(one_parts.OneText(name="TXT", value=value),),
    )


def _device_with_coroutine_handler(side_effect):
    class Device(Driver):
        name = "DEVICE"

        def __init__(self):
            super().__init__()
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

        @on(main.text.txt, Write)
        async def on_write(self, event):
            await self.side_effect(event)

    return Device()


def test_coroutine_write_handler_prevent_default():
    asyncio.run(_coroutine_write_handler_prevent_default())


async def _coroutine_write_handler_prevent_default():
    new_value = "ipsum"
    released = asyncio.Event()

    async def side_effect(event):
        event.prevent_default = True
        await released.wait()

    dev = _device_with_coroutine_handler(side_effect)
    assert dev.main.text.txt.value == "lorem"

    dev.message_from_client(_new_text(new_value))
    await asyncio.sleep(0)

    assert not released.is_set()
    assert dev.main.text.txt.value == "lorem"

    released.set()
    await asyncio.sleep(0)


def test_coroutine_write_handler_publishes_before_handler_finishes():
    asyncio.run(_coroutine_write_handler_publishes_before_handler_finishes())


async def _coroutine_write_handler_publishes_before_handler_finishes():
    new_value = "ipsum"
    released = asyncio.Event()

    async def side_effect(event):
        await released.wait()

    dev = _device_with_coroutine_handler(side_effect)
    assert dev.main.text.txt.value == "lorem"

    dev.message_from_client(_new_text(new_value))
    await asyncio.sleep(0)

    assert not released.is_set()
    assert dev.main.text.txt.value == new_value

    released.set()
    await asyncio.sleep(0)
