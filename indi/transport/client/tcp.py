import asyncio
import logging
from typing import Callable

from indi.message import IndiMessage
from indi.transport import Buffer

logger = logging.getLogger(__name__)


class ConnectionHandler:
    def __init__(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        callback: Callable[[IndiMessage], None],
    ):
        self.buffer = Buffer()
        self.reader, self.writer = reader, writer
        self.callback = callback
        self.sender_lock = asyncio.Lock()

    async def wait_for_messages(self):
        while True:
            logger.debug("TCP: waiting for data")
            message = await self.reader.read(1024)
            if not message:
                logger.debug("TCP: no data, breaking")
                break
            logger.debug("TCP: got data: %s", message)
            self.buffer.append(message.decode("latin1"))
            self.buffer.process(self.message_from_server)

    def message_from_server(self, message: IndiMessage):
        self.callback(message)

    def send_message(self, message: IndiMessage):
        data = message.to_string()
        asyncio.get_running_loop().create_task(self.send(data))

    async def send(self, data: bytes):
        async with self.sender_lock:
            logger.debug("TCP: sending data: %s", data)
            self.writer.write(data)
            await self.writer.drain()

    def close(self):
        self.writer.close()


class TCP:
    def __init__(self, address: str = "127.0.0.1", port: int = 7624):
        self.address = address
        self.port = port

    async def connect(self, callback: Callable[[IndiMessage], None]):
        reader, writer = await asyncio.open_connection(self.address, self.port)
        handler = ConnectionHandler(reader, writer, callback)
        return handler
