from indi.message.base import IndiMessage


@IndiMessage.register_message
class OneLight(IndiMessage):
    from_device = True

    def __init__(self, name: str, value, **junk):
        super().__init__()
        self.name = name
        self.value = value
