from typing import Optional

from indi.device import Driver, properties
from indi.device.events import Change, on
from indi.device.properties import standard
from indi.message import GetProperties
from indi.transport.client.tcp import TCP as TCPClient


class Proxy(Driver):
    """Virtual proxy device driver

    Connects to another INDI server and passes all messages in both ways.
    All devices from remote server become visible in INDIpy.
    """

    address: Optional[str] = None
    port = 7624

    general = properties.Group(
        "GENERAL",
        vectors=dict(
            connection=standard.common.Connection(),
        ),
    )

    def __init__(self, *args, **kwargs):
        self._connection = None
        self._client = TCPClient(self.address, self.port)
        super().__init__(*args, **kwargs)

    def message_from_client(self, message):
        if getattr(message, "device", None) in (None, self.name):
            super().message_from_client(message)

        if self._connection:
            self._connection.send_message(message)

    def _message_from_server(self, message):
        self._router.process_message(message, self)

    def accepts(self, device):
        return True

    @on(general.connection.connect, Change)
    def connect(self, sender):
        connected = self.get_group("general").connection.connect.bool_value
        if connected:
            self._connection = self._client.connect(self._message_from_server)
            self._connection.send_message(GetProperties(version="1.0"))
        else:
            if self._connection:
                self._connection.close()
            self._connection = None

    @property
    def client(self):
        return self._client
