import logging
import socket
import threading
import sys

from indi.routing import Client
from indi.transport import Buffer

logger = logging.getLogger(__name__)


class ConnectionHandler(Client):
    def __init__(self, router):
        self.buffer = Buffer()
        self.router = router
        self.sender_lock = threading.Lock()
        if self.router:
            self.router.register_client(self)

    def handle(self):
        try:
            self.wait_for_messages()
        except:
            logger.exception("")
            pass

        self.close()

    def wait_for_messages(self):
        while True:
            logger.debug(f"TTY: waiting for data")
            message = self._read()
            if not message:
                logger.debug(f"TTY: no data, breaking")
                break
            logger.debug(f"TTY: got data: {message}")
            self.buffer.append(message)
            self.buffer.process(self.message_from_client)

    def message_from_client(self, message):
        if self.router:
            self.router.process_message(message, sender=self)

    def message_from_device(self, message):
        data = message.to_string().decode("latin1")
        with self.sender_lock:
            logger.debug(f"TTY: sending data: {data}")
            self._write(data)

    def close(self):
        if self.router:
            self.router.unregister_client(self)

    def _read(self):
        return sys.stdin.readline()

    def _write(self, data):
        sys.stdout.write(data)
        sys.stdout.flush()


class TTY:
    def __init__(self, router=None):
        self.router = router

    def start(self):
        logger.info("Starting INDI server on TTY")
        conn_handler = ConnectionHandler(self.router)
        conn_handler.handle()
