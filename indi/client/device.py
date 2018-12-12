from indi import message
from indi.client.vectors import Vector


class Device:
    def __init__(self, client, name):
        self.vectors = {}
        self.client = client
        self.name = name

    def __getitem__(self, key):
        return self.vectors[key]

    def __contains__(self, key):
        return key in self.vectors

    def get_vector(self, name):
        return self.vectors.get(name)

    def set_vector(self, name, vector):
        self.vectors[name] = vector

    def process_message(self, msg):
        vector = None
        if isinstance(msg, message.DefVector):
            vector = Vector.from_message(self, msg)
            self.set_vector(msg.name, vector)
            self.client.trigger_change(vector, 'definition')

        if isinstance(msg, message.SetVector):
            vector = self.get_vector(msg.name)

        if isinstance(msg, message.DelProperty):
            if msg.name in self.vectors:
                del self.vectors[msg.name]
            vector = None

        if vector:
            vector.process_message(msg)

    def send_message(self, msg):
        self.client.send_message(msg)
