import logging

from indi.message import EnableBLOB, NewBLOBVector, const

logger = logging.getLogger(__name__)


class Router:
    """Message router

    Passess messages between device drivers and client connections.
    """

    _instance = None

    DEFAULT_BLOB_POLICY = const.BLOBEnable.NEVER

    def __init__(self):
        self.clients = []
        self.devices = []
        self.blob_routing = {}

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def register_device(self, device):
        self.devices.append(device)

    def register_client(self, client):
        logger.debug("Router: registering client %s", client)
        self.clients.append(client)
        self.blob_routing[client] = {}

    def unregister_client(self, client):
        logger.debug("Router: unregistering client %s", client)
        if client in self.clients:
            self.clients.remove(client)
        if client in self.blob_routing:
            del self.blob_routing[client]

    def process_message(self, message, sender=None):
        is_blob = isinstance(message, NewBLOBVector)

        if message.from_client:
            if isinstance(message, EnableBLOB):
                self.process_enable_blob(message, sender)

            for device in self.devices:
                if not device == sender and (
                    not message.device or device.accepts(message.device)
                ):
                    device.message_from_client(message)

        if message.from_device:
            for client in self.clients:
                if not client == sender:
                    device = getattr(message, "device", None)
                    client_blob_policy = self.blob_routing.get(client, {}).get(
                        device, self.DEFAULT_BLOB_POLICY
                    )
                    if (
                        is_blob
                        and client_blob_policy
                        in (
                            const.BLOBEnable.ALSO,
                            const.BLOBEnable.ONLY,
                        )
                    ) or (not is_blob and client_blob_policy == const.BLOBEnable.NEVER):
                        client.message_from_device(message)

    def process_enable_blob(self, message, sender):
        self.blob_routing[sender][message.name] = message.value
