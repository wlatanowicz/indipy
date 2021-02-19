from typing import Dict, List, Type

from indi.device import Driver
from indi.routing import Router


class DevicePool:
    def __init__(self):
        self.device_classes: List[type] = []
        self.devices: Dict[str, Driver] = {}

    def register(self, device_class: Type[Driver]):
        self.device_classes.append(device_class)
        return device_class

    def init(self, router: Router):
        for device_class in self.device_classes:
            dev = device_class(router=router)
            self.devices[dev.name] = dev

    def get(self, name: str) -> Driver:
        return self.devices[name]


default_pool = DevicePool()
