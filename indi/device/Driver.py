from .properties.instance.group import Group
from .properties import Group as GroupDefinition
from ..routing import Device

from .. import message

import logging


class DriverMeta(type):
    def __new__(meta, name, bases, dct):
        for k in dct:
            if isinstance(dct[k], GroupDefinition):
                dct[k].property_name = k

        return super().__new__(meta, name, bases, dct)


class Driver(Device, metaclass=DriverMeta):
    onchange = None

    def __init__(self, name=None, router=None):
        if name is not None:
            self._name = name
        elif self.__class__.name is not None:
            self._name = self.__class__.name

        self._groups = {k: Group(self, v) for k, v in self.__class__.__dict__.items() if isinstance(v, GroupDefinition)}
        self._router = router

        self._vectors = {}
        for k, group in self._groups.items():
            for k, vector in group.vectors.items():
                self._vectors[vector.name] = vector

        if self._router:
            self._router.register_device(self)

    @property
    def name(self):
        return self._name

    @property
    def routing_key(self):
        return self._name
        
    def get_group(self, name):
        return self._groups.get(name)

    def send_message(self, msg):
        if self._router and msg:
            self._router.process_message(msg, self)

    def message_from_client(self, msg):
        if isinstance(msg, message.GetProperties):
            if not msg.name:
                for k, v in self._vectors.items():
                    self.send_message(v.to_def_message())
                for k, v in self._vectors.items():
                    self.send_message(v.to_set_message())
            else:
                v = self._vectors[msg.name]
                self.send_message(v.to_def_message())
                self.send_message(v.to_set_message())

        if isinstance(msg, message.news.NewVector):
            self._vectors[msg.name].from_new_message(msg)

    def trigger_callback(self, callback, sender, **kwargs):
        if not callback:
            return

        if isinstance(callback, str):
            callback = getattr(self, callback)

        try:
            callback(sender, **kwargs)
        except Exception as e:
            logging.exception(e)
