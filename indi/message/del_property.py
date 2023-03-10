from indi.message.base import IndiMessage


class DelProperty(IndiMessage):
    from_device = True

    def __init__(self, device, name=None, timestamp=None, message=None, **junk):
        super().__init__(device)
        self.name = name
        self.timestamp = timestamp
        self.message = message
