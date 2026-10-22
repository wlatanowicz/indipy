from indi.message.base import IndiMessage


@IndiMessage.register_message
class GetProperties(IndiMessage):
    from_device = True
    from_client = True

    def __init__(self, version: str, device: str | None = None, name: str | None = None, **junk):
        super().__init__(device)
        self.version = version
        self.name = name
