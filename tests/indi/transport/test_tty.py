import asyncio
from unittest.mock import Mock

from indi.message import DelProperty
from indi.routing import Router
from indi.transport.server.tty import ConnectionHandler


class YieldingStdout:
    def __init__(self) -> None:
        self.chars: list[str] = []
        self.events: list[tuple[str, str] | str] = []
        self.in_flight = 0
        self.max_in_flight = 0

    async def write(self, data: str) -> None:
        self.in_flight += 1
        self.max_in_flight = max(self.max_in_flight, self.in_flight)
        self.events.append(("write-start", data))
        try:
            for char in data:
                self.chars.append(char)
                await asyncio.sleep(0)
        finally:
            self.in_flight -= 1
        self.events.append(("write-end", data))

    async def flush(self) -> None:
        self.events.append("flush")
        await asyncio.sleep(0)


def test_overlapping_tty_writes_stay_whole_and_in_order():
    asyncio.run(_send_two_messages())


async def _send_two_messages():
    stdout = YieldingStdout()
    handler = ConnectionHandler(Router(), stdin=Mock(), stdout=stdout)
    first = DelProperty(device="Camera", name="EXPOSURE")
    second = DelProperty(device="Focuser", name="POSITION")

    handler.message_from_device(first)
    handler.message_from_device(second)

    writes = {task for task in asyncio.all_tasks() if task is not asyncio.current_task()}
    done, pending = await asyncio.wait(writes, timeout=2)
    assert not pending
    for task in done:
        task.result()

    first_text = first.to_string().decode("latin1")
    second_text = second.to_string().decode("latin1")
    assert stdout.max_in_flight == 1
    assert "".join(stdout.chars) == first_text + second_text
    assert stdout.events == [
        ("write-start", first_text),
        ("write-end", first_text),
        "flush",
        ("write-start", second_text),
        ("write-end", second_text),
        "flush",
    ]
