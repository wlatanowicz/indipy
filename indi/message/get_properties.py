from indi.message.base import IndiMessage


class GetProperties(IndiMessage):
    from_device = True
    from_client = True

    def __init__(self, version, device=None, name=None, **junk):
        super().__init__(device)
        self.version = version
        self.name = name
