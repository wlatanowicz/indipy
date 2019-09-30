from typing import Dict, List, Type

from indi.device import Driver
from indi.routing import Router


class DevicePool:
    device_classes: List[type] = []

    devices: Dict[str, Driver] = {}

    @classmethod
    def register(cls, device_class: Type[Driver]):
        cls.device_classes.append(device_class)

    @classmethod
    def init(cls, router: Router):
        for device_class in cls.device_classes:
            dev = device_class(router=router)
            cls.devices[dev.name] = dev

    @classmethod
    def get(cls, name: str) -> Driver:
        return cls.devices[name]
