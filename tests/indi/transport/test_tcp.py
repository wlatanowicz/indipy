import asyncio
from unittest.mock import Mock

from indi.message import IndiMessage
from indi.transport.server.tcp import ConnectionHandler


class _RaisingRouter:
    def __init__(self) -> None:
        self.names: list[str | None] = []

    def register_client(self, client: object) -> None:
        pass

    def process_message(self, message: IndiMessage, sender: object = None) -> None:
        self.names.append(message.name)
        if message.name == "BAD":
            raise RuntimeError("bad message")


def test_tcp_read_loop_continues_after_handler_error():
    asyncio.run(_tcp_survives_bad_message())


async def _tcp_survives_bad_message():
    router = _RaisingRouter()
    reader = asyncio.StreamReader()
    reader.feed_data(
        b'<getProperties version="1.0" device="Camera" name="BAD" />'
        b'<getProperties version="1.0" device="Camera" name="GOOD" />'
    )
    reader.feed_eof()
    handler = ConnectionHandler(reader, Mock(), router)

    await handler.wait_for_messages()

    assert router.names == ["BAD", "GOOD"]
