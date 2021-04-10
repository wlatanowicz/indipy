import logging
import socket
import threading

from indi.routing import Client
from indi.transport import Buffer

logger = logging.getLogger(__name__)


class ConnectionHandler(Client):
    connections = []

    def __init__(self, client_socket, router):
        self.buffer = Buffer()
        self.client_socket = client_socket
        self.router = router
        self.sender_lock = threading.Lock()
        if self.router:
            self.router.register_client(self)

    @classmethod
    def handler(cls, router):
        def handler_func(client_socket):
            conn = cls(client_socket, router)
            cls.connections.append(conn)
            try:
                conn.wait_for_messages()
            except:
                logger.exception("Error in client handler loop")

            conn.close()
            cls.connections.remove(conn)

        return handler_func

    def wait_for_messages(self):
        while True:
            logger.debug(f"TCP: waiting for data")
            message = self.client_socket.recv(1024)
            if not message:
                logger.debug(f"TCP: no data, breaking")
                break
            logger.debug(f"TCP: got data: {message}")
            self.buffer.append(message.decode("latin1"))
            self.buffer.process(self.message_from_client)

    def message_from_client(self, message):
        if self.router:
            self.router.process_message(message, sender=self)

    def message_from_device(self, message):
        data = message.to_string()

        def send():
            with self.sender_lock:
                logger.debug(f"TCP: sending data: {data}")
                self.client_socket.sendall(data)

        th = threading.Thread(target=send, daemon=True)
        th.start()

    def close(self):
        if self.client_socket:
            self.client_socket.close()
        if self.router:
            self.router.unregister_client(self)


class TCP:
    def __init__(self, address="0.0.0.0", port=7624, max_connections=5, router=None):
        self.address = address
        self.port = port
        self.max_connections = max_connections
        self.router = router

    def start(self):
        logger.info("Starting TCP INDI server on %s:%s", self.address, self.port)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(
            (
                self.address,
                self.port,
            )
        )
        server.listen(self.max_connections)

        try:
            while True:
                client_sock, address = server.accept()
                logger.info(
                    "Accepted connection from {}:{}".format(address[0], address[1])
                )
                client_handler = threading.Thread(
                    target=ConnectionHandler.handler(self.router),
                    args=(client_sock,),
                    daemon=True,
                )
                client_handler.start()
        except:
            for conn in ConnectionHandler.connections:
                conn.close()
            if server:
                server.close()
