from indi.device.events import EventSourceDefinition
from indi.device.properties.definition.vectors import Vector


class Group(EventSourceDefinition):
    def __init__(self, name: str, enabled=True, vectors: dict[str, Vector] | None = None):
        super().__init__()
        self.name = name
        self.vectors: dict[str, Vector] = vectors or {}
        self.enabled = enabled

    def __getattr__(self, item: str):
        vector = self.vectors.get(item)
        if vector:
            return vector

        return self.__getattribute__(item)
