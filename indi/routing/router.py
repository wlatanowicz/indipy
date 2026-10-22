import logging
from typing import TypeAlias

from indi.message import DefBLOBVector, EnableBLOB, IndiMessage, SetBLOBVector, const
from indi.routing import Client, Device

logger = logging.getLogger(__name__)


SenderType: TypeAlias = Client | Device | None


class Router:
    """Message router

    Passess messages between device drivers and client connections.
    """

    _instance = None

    DEFAULT_BLOB_POLICY = const.BLOBEnable.NEVER

    def __init__(self) -> None:
        self.clients: list[Client] = []
        self.devices: list[Device] = []
        self.blob_routing: dict[SenderType, dict[str | None, const.BLOBEnableType]] = {}

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def register_device(self, device: Device):
        self.devices.append(device)

    def register_client(self, client: Client):
        logger.debug("Router: registering client %s", client)
        self.clients.append(client)
        self.blob_routing[client] = {}

    def unregister_client(self, client: Client):
        logger.debug("Router: unregistering client %s", client)
        if client in self.clients:
            self.clients.remove(client)
        if client in self.blob_routing:
            del self.blob_routing[client]

    def process_message(self, message: IndiMessage, sender: SenderType = None):
        if message.from_client:
            if isinstance(message, EnableBLOB):
                self.process_enable_blob(message, sender)

            for device in self.devices:
                if device != sender and device.accepts(message.device):
                    device.message_from_client(message)

        if message.from_device:
            is_blob = isinstance(message, DefBLOBVector | SetBLOBVector)
            for client in self.clients:
                if client != sender and self._forwards_to_client(client, message.device, is_blob):
                    client.message_from_device(message)

    def _forwards_to_client(self, client: Client, device_name: str | None, is_blob: bool) -> bool:
        policy = self.blob_routing.get(client, {}).get(device_name, self.DEFAULT_BLOB_POLICY)
        if policy == const.BLOBEnable.ONLY:
            return is_blob
        if policy == const.BLOBEnable.ALSO:
            return True
        return not is_blob

    def process_enable_blob(self, message: EnableBLOB, sender: SenderType):
        self.blob_routing[sender][message.device] = message.value
