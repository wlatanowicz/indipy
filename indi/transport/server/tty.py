import logging
import aiofiles
import asyncio

from indi.routing import Client
from indi.transport import Buffer

logger = logging.getLogger(__name__)


class ConnectionHandler(Client):
    def __init__(self, router, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout
        self.buffer = Buffer()
        self.router = router
        if self.router:
            self.router.register_client(self)

    async def handle(self):
        try:
            await self.wait_for_messages()
        except:
            logger.exception("Error in client handler loop")

        logger.info("Stopping INDIpy server on TTY")
        self.close()

    async def wait_for_messages(self):
        while True:
            logger.debug(f"Waiting for data")
            message = await self._read()
            if not message:
                logger.debug(f"No data, exiting")
                break
            logger.debug("Received data: %s", message)
            self.buffer.append(message)
            self.buffer.process(self.message_from_client)

    def message_from_client(self, message):
        if self.router:
            self.router.process_message(message, sender=self)

    def message_from_device(self, message):
        data = message.to_string().decode("latin1")
        logger.debug("Sending data: %s", data)
        asyncio.get_running_loop().create_task(self._write(data))

    def close(self):
        if self.router:
            self.router.unregister_client(self)

    async def _read(self):
        return await self.stdin.readline()

    async def _write(self, data):
        await self.stdout.write(data)
        await self.stdout.flush()


class TTY:
    def __init__(self, router=None, stdin=None, stdout=None):
        self.router = router
        self.stdin = stdin or aiofiles.stdin
        self.stdout = stdout or aiofiles.stdout

    def start(self):
        logger.info("Starting INDIpy server on TTY")
        conn_handler = ConnectionHandler(self.router, self.stdin, self.stdout)
        asyncio.run(conn_handler.handle())
