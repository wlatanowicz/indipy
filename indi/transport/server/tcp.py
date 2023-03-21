import asyncio
import logging
from typing import List

from indi.message import IndiMessage
from indi.routing import Client, Router
from indi.transport import Buffer

logger = logging.getLogger(__name__)


class ConnectionHandler(Client):
    connections: List["ConnectionHandler"] = []

    def __init__(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, router: Router
    ):
        self.buffer = Buffer()
        self.reader, self.writer = reader, writer
        self.router = router
        self.sender_lock = asyncio.Lock()
        if self.router:
            self.router.register_client(self)

    @classmethod
    def handler(cls, router: Router):
        async def handler_func(reader, writer):
            conn = cls(reader, writer, router)
            cls.connections.append(conn)
            try:
                await conn.wait_for_messages()
            except:
                logger.exception("Error in client handler loop")

            conn.close()
            cls.connections.remove(conn)

        return handler_func

    async def wait_for_messages(self):
        while True:
            logger.debug(f"TCP: waiting for data")
            message = await self.reader.read(1024)
            if not message:
                logger.debug(f"TCP: no data, breaking")
                break
            logger.debug("TCP: got data: %s", message)
            self.buffer.append(message.decode("latin1"))
            self.buffer.process(self.message_from_client)

    def message_from_client(self, message: IndiMessage):
        if self.router:
            self.router.process_message(message, sender=self)

    def message_from_device(self, message: IndiMessage):
        data = message.to_string()
        asyncio.get_running_loop().create_task(self.send(data))

    async def send(self, data: bytes):
        async with self.sender_lock:
            logger.debug("TCP: sending data: %s", data)
            self.writer.write(data)
            await self.writer.drain()

    def close(self):
        self.writer.close()
        if self.router:
            self.router.unregister_client(self)


class TCP:
    def __init__(self, router: Router, address="0.0.0.0", port=7624):
        self.address = address
        self.port = port
        self.router = router

    async def client_connected(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        handler = ConnectionHandler.handler(self.router)
        await handler(reader, writer)

    async def start(self):
        logger.info("Starting async TCP INDI server on %s:%s", self.address, self.port)
        server = await asyncio.start_server(
            self.client_connected, self.address, self.port
        )

        try:
            async with server:
                await server.serve_forever()
        finally:
            for conn in ConnectionHandler.connections:
                conn.close()
