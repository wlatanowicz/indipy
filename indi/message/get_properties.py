from indi.message.base import IndiMessage


class GetProperties(IndiMessage):
    from_device = True
    from_client = True

    def __init__(self, version, device=None, name=None, **junk):
        self.version = version
        self.device = device
        self.name = name
