import asyncio
from unittest.mock import Mock

from indi.message import DelProperty, IndiMessage
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
        await asyncio.sleep(0)
        self.events.append("flush")


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


class _ScriptedStdin:
    def __init__(self, lines: list[str]) -> None:
        self._lines = list(lines)

    async def readline(self) -> str:
        if not self._lines:
            return ""
        return self._lines.pop(0)


class _RaisingRouter:
    def __init__(self) -> None:
        self.names: list[str | None] = []

    def register_client(self, client: object) -> None:
        pass

    def process_message(self, message: IndiMessage, sender: object = None) -> None:
        self.names.append(message.name)
        if message.name == "BAD":
            raise RuntimeError("bad message")


def test_tty_read_loop_continues_after_handler_error():
    asyncio.run(_tty_survives_bad_message())


async def _tty_survives_bad_message():
    router = _RaisingRouter()
    chunk = (
        '<getProperties version="1.0" device="Camera" name="BAD" />'
        '<getProperties version="1.0" device="Camera" name="GOOD" />\n'
    )
    stdin = _ScriptedStdin([chunk])
    handler = ConnectionHandler(router, stdin=stdin, stdout=Mock())

    await handler.wait_for_messages()

    assert router.names == ["BAD", "GOOD"]
