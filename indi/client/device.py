from typing import Optional

from indi import message
from indi.client.client import Client
from indi.client.vectors import Vector


class Device:
    def __init__(self, client: Client, name: str):
        self.vectors = {}
        self.client = client
        self.name = name

    def __getitem__(self, key) -> Vector:
        return self.vectors[key]

    def __contains__(self, key) -> bool:
        return key in self.vectors

    def get_vector(self, name) -> Optional[Vector]:
        return self.vectors.get(name)

    def set_vector(self, name: str, vector: Vector):
        self.vectors[name] = vector

    def process_message(self, msg: message.IndiMessage):
        vector = None
        if isinstance(msg, message.DefVector):
            vector = Vector.from_message(self, msg)
            self.set_vector(msg.name, vector)
            self.client.trigger_update(vector, "definition")

        if isinstance(msg, message.SetVector):
            vector = self.get_vector(msg.name)

        if isinstance(msg, message.DelProperty):
            if msg.name in self.vectors:
                del self.vectors[msg.name]
            vector = None

        if vector:
            vector.process_message(msg)

    def send_message(self, msg: message.IndiMessage):
        self.client.send_message(msg)
