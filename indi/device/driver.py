from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Dict, Optional, Type, cast

from indi import message
from indi.device.events import attach_event_handlers
from indi.device.properties import Group as GroupDefinition
from indi.device.properties.instance.group import Group, GroupGetter
from indi.device.properties.instance.vectors import Vector
from indi.message import IndiMessage
from indi.routing import Device, Router

if TYPE_CHECKING:
    from indi.device.snoop import SnoopingClient

logger = logging.getLogger(__name__)


class DriverMeta(type):
    def __new__(meta, name, bases, dct):
        groups = {}
        for k in dct:
            if isinstance(dct[k], GroupDefinition):
                groups[k] = dct[k]
                dct[k] = GroupGetter(k)
        dct["_group_definitions"] = groups

        return super().__new__(meta, name, bases, dct)


class Driver(Device, metaclass=DriverMeta):
    _group_definitions: Dict[str, GroupDefinition] = {}

    def __init__(self, name: Optional[str] = None, router: Optional[Router] = None):
        attach_event_handlers(self)

        self._name: str = name or str(self.__class__.name)

        self._groups: Dict[str, Group] = {
            k: Group(self, v)
            for k, v in self.__class__._all_group_definitions().items()
        }
        self._router = router

        self._vectors: Dict[str, Vector] = {}
        for k, group in self._groups.items():
            for k, vector in group.vectors.items():
                self._vectors[vector.name] = vector

        if self._router:
            self._router.register_device(self)
        self._snooping_client: Optional[SnoopingClient] = None

    @property
    def snooping_client(self) -> SnoopingClient:
        from indi.device.snoop import SnoopingClient

        assert (
            self._router
        ), "Router has to be defined before creating a snooping client"

        if self._snooping_client is None:
            self._snooping_client = SnoopingClient(self._router)
            self._router.register_client(self._snooping_client)
        return self._snooping_client

    def snoop_device(self, device: str, name: Optional[str] = None) -> SnoopingClient:
        client = self.snooping_client
        client.handshake(device, name)
        return client

    @classmethod
    def _all_group_definitions(cls) -> Dict[str, GroupDefinition]:
        groups: Dict[str, GroupDefinition] = {}
        for base in cls.__bases__:
            if issubclass(base, Driver) or base is Driver:
                groups = {**groups, **cast(Type[Driver], base)._group_definitions}
        for k, v in cls._group_definitions.items():
            if isinstance(v, GroupDefinition):
                groups[k] = v
        return groups

    @property
    def name(self) -> str:
        return self._name

    def accepts(self, device: Optional[str]) -> bool:
        return device is None or self.name == device

    def get_group(self, name: str) -> Optional[Group]:
        return self._groups.get(name)

    def send_message(self, msg: Optional[IndiMessage]):
        if self._router and msg:
            self._router.process_message(msg, self)

    def message_from_client(self, msg: IndiMessage):
        if isinstance(msg, message.GetProperties):
            if not msg.name:
                for k, v in self._vectors.items():
                    self.send_message(v.to_def_message())
            else:
                if msg.name in self._vectors:
                    v = self._vectors[msg.name]
                    self.send_message(v.to_def_message())

        if isinstance(msg, message.news.NewVector):
            self._vectors[msg.name].from_new_message(msg)
