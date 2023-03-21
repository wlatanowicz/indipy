from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from indi.device.properties.definition.group import Group as GroupDefinition
from indi.device.properties.instance.vectors import Vector

if TYPE_CHECKING:
    from indi.device.driver import Driver


class Group:
    def __init__(self, device: Driver, definition: GroupDefinition) -> None:
        self._device = device
        self._definition: GroupDefinition = definition
        self._vectors: Dict[str, Vector] = {
            k: v.instance(self) for k, v in definition.vectors.items()
        }
        self._enabled = definition.enabled

    def __getattr__(self, item):
        vector = self._vectors.get(item)
        if vector:
            return vector

        return self.__getattribute__(item)

    @property
    def device(self) -> Driver:
        return self._device

    @property
    def name(self) -> str:
        return self._definition.name

    @property
    def vectors(self) -> Dict[str, Vector]:
        return self._vectors

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value
        for k, v in self._vectors.items():
            self.device.send_message(v.to_def_message())
            self.device.send_message(v.to_set_message())


class GroupGetter:
    def __init__(self, property_name: str):
        self.property_name = property_name

    def __get__(self, instance: Driver, objtype=None):
        assert self.property_name
        return instance.get_group(self.property_name)
