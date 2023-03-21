import logging
from typing import Dict, List, Optional, Union, cast

from indi.message import EnableBLOB, IndiMessage, NewBLOBVector, const
from indi.routing import Client, Device

logger = logging.getLogger(__name__)


SenderType = Optional[Union[Client, Device]]


class Router:
    """Message router

    Passess messages between device drivers and client connections.
    """

    _instance = None

    DEFAULT_BLOB_POLICY = const.BLOBEnable.NEVER

    def __init__(self) -> None:
        self.clients: List[Client] = []
        self.devices: List[Device] = []
        self.blob_routing: Dict[
            SenderType, Dict[Optional[str], const.BLOBEnableType]
        ] = {}

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
        is_blob = isinstance(message, NewBLOBVector)

        if message.from_client:
            if isinstance(message, EnableBLOB):
                self.process_enable_blob(message, sender)

            for device in self.devices:
                if not device == sender and device.accepts(message.device):
                    device.message_from_client(message)

        if message.from_device:
            for client in self.clients:
                if not client == sender:
                    device_name = getattr(message, "device")
                    client_blob_policy = self.blob_routing.get(client, {}).get(
                        device_name, self.DEFAULT_BLOB_POLICY
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

    def process_enable_blob(self, message: EnableBLOB, sender: SenderType):
        self.blob_routing[sender][message.device] = message.value
