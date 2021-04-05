from typing import Optional

from indi.device.properties.definition.group import Group as GroupDefinition


class Group:
    def __init__(self, device, definition):
        self._device = device
        self._definition: GroupDefinition = definition
        self._vectors = {k: v.instance(self) for k, v in definition.vectors.items()}
        self._enabled = definition.enabled

    def __getattr__(self, item):
        vector = self._vectors.get(item)
        if vector:
            return vector

        return self.__getattribute__(item)

    @property
    def device(self):
        return self._device

    @property
    def name(self):
        return self._definition.name

    @property
    def vectors(self):
        return self._vectors

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
        for k, v in self._vectors.items():
            self.device.send_message(v.to_def_message())
            self.device.send_message(v.to_set_message())
