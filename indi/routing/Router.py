import logging
import threading
from indi.message import const
from indi.message import NewBLOBVector, EnableBLOB


class Router:
    instance = None

    def __init__(self):
        self.clients = []
        self.devices = []
        self.blob_routing = {}

    @classmethod
    def instance(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance

    def register_device(self, device):
        self.devices.append(device)
        for client in self.clients:
            self.blob_routing[client][device.routing_key] = const.BLOBEnable.NEVER

    def register_client(self, client):
        logging.debug('Router: registering client %s', client)
        self.clients.append(client)
        self.blob_routing[client] = {d.routing_key: const.BLOBEnable.NEVER for d in self.devices}

    def unregister_client(self, client):
        logging.debug('Router: unregistering client %s', client)
        if client in self.clients:
            self.clients.remove(client)
        if self.blob_routing.get(client):
            del self.blob_routing[client]

    def process_message(self, message, sender=None):
        is_blob = isinstance(message, NewBLOBVector)

        if message.from_client:
            if isinstance(message, EnableBLOB):
                self.process_enable_blob(message, sender)

            for device in self.devices:
                if not device == sender and (not message.device or message.device == device.routing_key):
                    device.message_from_client(message)

        if message.from_device:
            for client in self.clients:
                if not client == sender:
                    if sender is None and not is_blob \
                            or (is_blob and self.blob_routing[client][sender.routing_key] in (const.BLOBEnable.ALSO, const.BLOBEnable.ONLY,)) \
                            or (not is_blob and self.blob_routing[client][sender.routing_key] == const.BLOBEnable.NEVER):

                        def send():
                            client.message_from_device(message)

                        th = threading.Thread(target=send, daemon=True)
                        th.start()


    def process_enable_blob(self, message, sender):
        self.blob_routing[sender][message.name] = message.value
