from typing import Dict, List, Type

from indi.device import Driver
from indi.routing import Router


class DevicePool:
    """Device driver registry.

    In most cases you want to use preinitialized `default_pool`.
    """

    def __init__(self):
        self.device_classes: List[type] = []
        self.devices: Dict[str, Driver] = {}

    def register(self, device_class: Type[Driver]) -> Type[Driver]:
        """Register device

        Register device driver class in device pool.
        Designed to be used as decorator.

        :param device_class: Device to be registered
        :type device_class: Type[Driver]
        :return: Unmodified device class
        :rtype: Type[Driver]
        """
        self.device_classes.append(device_class)
        return device_class

    def init(self, router: Router):
        """Initialize all devices registered in the device pool

        :param router: Router instance responsible for handling communication
        :type router: Router
        """
        for device_class in self.device_classes:
            dev = device_class(router=router)
            self.devices[dev.name] = dev

    def get(self, name: str) -> Driver:
        """Get device driver instance by name

        :param name: Device name
        :type name: str
        :return: Device driver instance
        :rtype: Driver
        """
        return self.devices[name]


default_pool = DevicePool()
