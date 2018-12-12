from indi.message.IndiMessage import IndiMessage


class Message(IndiMessage):
    from_device = True

    def __init__(self, device=None, timestamp=None, message=None, **junk):
        self.device = device
        self.timestamp = timestamp
        self.message = message
