import logging

from websocket_server import WebsocketServer

from indi.message import IndiMessage
from indi.routing import Client

logger = logging.getLogger(__name__)


class ConnectionHandler(Client):
    def __init__(self, server, client, router):
        self.server = server
        self.client = client
        self.router = router

    def message_from_device(self, message):
        data = message.to_string()

        def send():
            try:
                self.server.send_message(self.client, data)
            except:
                pass

        th = threading.Thread(target=send, daemon=True)
        th.start()

    def message_from_client(self, message):
        if self.router:
            self.router.process_message(message, sender=self)

    def text_message_from_client(self, text_message):
        message = IndiMessage.from_string(text_message)
        self.message_from_client(message)


class WebSocket:
    def __init__(self, address="0.0.0.0", port=8001, router=None):
        self.address = address
        self.port = port
        self.router = router
        self.clients = {}

    def start(self):
        logger.info("Starting WebSocket INDI server on %s:%s", self.address, self.port)
        server = WebsocketServer(self.port, host=self.address)
        server.set_fn_new_client(self._new_client)
        server.set_fn_client_left(self._client_left)
        server.set_fn_message_received(self._message_received)
        server.run_forever()

    def _new_client(self, client, server):
        handler = ConnectionHandler(server, client, self.router)
        self.clients[client["id"]] = handler
        self.router.register_client(handler)

    def _client_left(self, client, server):
        if client:
            handler = self.clients[client["id"]]
            del self.clients[client["id"]]
            self.router.unregister_client(handler)

    def _message_received(self, client, server, message):
        self.clients[client["id"]].text_message_from_client(message)
