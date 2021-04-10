import logging
from typing import Callable, Dict, Optional, Union

from indi import message
from indi.device.events import attach_event_handlers
from indi.device.properties import Group as GroupDefinition
from indi.device.properties.definition.vectors import Vector
from indi.device.properties.instance.group import Group
from indi.message import IndiMessage
from indi.routing import Device, Router


class DriverMeta(type):
    def __new__(meta, name, bases, dct):
        for k in dct:
            if isinstance(dct[k], GroupDefinition):
                dct[k].property_name = k

        return super().__new__(meta, name, bases, dct)


class Driver(Device, metaclass=DriverMeta):
    def __init__(self, name: Optional[str] = None, router: Optional[Router] = None):
        attach_event_handlers(self)

        if name is not None:
            self._name = name
        elif self.__class__.name is not None:
            self._name = self.__class__.name

        self._groups: Dict[str, Group] = {
            k: Group(self, v) for k, v in self.__class__._group_definitions().items()
        }
        self._router = router

        self._vectors: Dict[str, Vector] = {}
        for k, group in self._groups.items():
            for k, vector in group.vectors.items():
                self._vectors[vector.name] = vector

        if self._router:
            self._router.register_device(self)

    @classmethod
    def _group_definitions(cls) -> Dict[str, GroupDefinition]:
        groups: Dict[str, GroupDefinition] = {}
        for base in cls.__bases__:
            if issubclass(base, Driver) or base is Driver:
                groups = {**groups, **base._group_definitions()}
        for k, v in cls.__dict__.items():
            if isinstance(v, GroupDefinition):
                groups[k] = v
        return groups

    @property
    def name(self) -> Optional[str]:
        return self._name

    def accepts(self, device: str) -> bool:
        return self.name == device

    def get_group(self, name: str) -> Optional[Group]:
        return self._groups.get(name)

    def send_message(self, msg: IndiMessage):
        if self._router and msg:
            self._router.process_message(msg, self)

    def message_from_client(self, msg: IndiMessage):
        if isinstance(msg, message.GetProperties):
            if not msg.name:
                for k, v in self._vectors.items():
                    self.send_message(v.to_def_message())
            else:
                v = self._vectors[msg.name]
                self.send_message(v.to_def_message())

        if isinstance(msg, message.news.NewVector):
            self._vectors[msg.name].from_new_message(msg)

    def trigger_callback(
        self, callback: Optional[Union[str, Callable]], sender, **kwargs
    ):
        if not callback:
            return

        if isinstance(callback, str):
            callback_fun = getattr(self, callback)
        else:
            callback_fun = callback

        try:
            callback_fun(sender, **kwargs)
        except Exception as e:
            logging.exception(e)
