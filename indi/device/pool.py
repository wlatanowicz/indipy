class DevicePool:
    device_classes = []

    devices = {}

    @classmethod
    def register(cls, device_class):
        cls.device_classes.append(device_class)

    @classmethod
    def init(cls, router):
        for device_class in cls.device_classes:
            dev = device_class(router=router)
            cls.devices[dev.name] = dev

    @classmethod
    def get(cls, name):
        return cls.devices[name]
