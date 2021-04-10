import logging
import socket
import sys
import threading

from indi.routing import Client
from indi.transport import Buffer

logger = logging.getLogger(__name__)


class ConnectionHandler(Client):
    def __init__(self, router, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout
        self.buffer = Buffer()
        self.router = router
        self.sender_lock = threading.Lock()
        if self.router:
            self.router.register_client(self)

    def handle(self):
        try:
            self.wait_for_messages()
        except:
            logger.exception("Error in client handler loop")

        logger.info("Stopping INDIpy server on TTY")
        self.close()

    def wait_for_messages(self):
        while True:
            logger.debug(f"Waiting for data")
            message = self._read()
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

        def send():
            with self.sender_lock:
                logger.debug("Sending data: %s", data)
                self._write(data)

        th = threading.Thread(target=send, daemon=True)
        th.start()

    def close(self):
        if self.router:
            self.router.unregister_client(self)

    def _read(self):
        return self.stdin.readline()

    def _write(self, data):
        self.stdout.write(data)
        self.stdout.flush()


class TTY:
    def __init__(self, router=None, stdin=None, stdout=None):
        self.router = router
        self.stdin = stdin or sys.stdin
        self.stdout = stdout or sys.stdout

    def start(self):
        logger.info("Starting INDIpy server on TTY")
        conn_handler = ConnectionHandler(self.router, self.stdin, self.stdout)
        conn_handler.handle()
