from typing import Optional

from indi.typing import Callback


class Group:
    def __init__(
        self, name: str, enabled=True, onchange: Optional[Callback] = None, vectors=None
    ):
        self.name = name
        self.vectors = vectors
        self.property_name = None
        self.onchange = onchange
        self.enabled = enabled

    def __get__(self, instance, objtype=None):
        return instance.get_group(self.property_name)

    def __getattr__(self, item):
        vector = self.vectors.get(item)
        if vector:
            return vector

        return self.__getattribute__(item)
