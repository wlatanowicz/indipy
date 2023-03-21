from typing import Dict, Optional

from indi.device.events import EventSourceDefinition
from indi.device.properties.definition.vectors import Vector


class Group(EventSourceDefinition):
    def __init__(
        self, name: str, enabled=True, vectors: Optional[Dict[str, Vector]] = None
    ):
        super().__init__()
        self.name = name
        self.vectors: Dict[str, Vector] = vectors or {}
        self.enabled = enabled

    def __getattr__(self, item: str):
        vector = self.vectors.get(item)
        if vector:
            return vector

        return self.__getattribute__(item)
