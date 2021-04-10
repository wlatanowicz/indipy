from typing import Optional

from indi.device.events import EventSourceDefinition


class Group(EventSourceDefinition):
    def __init__(self, name: str, enabled=True, vectors=None):
        super().__init__()
        self.name = name
        self.vectors = vectors
        self.property_name = None
        self.enabled = enabled

    def __get__(self, instance, objtype=None):
        return instance.get_group(self.property_name)

    def __getattr__(self, item):
        vector = self.vectors.get(item)
        if vector:
            return vector

        return self.__getattribute__(item)
