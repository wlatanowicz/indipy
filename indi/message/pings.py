from indi.message.base import IndiMessage


@IndiMessage.register_message
class PingReply(IndiMessage):
    from_client = True

    def __init__(self, uid: str, **junk):
        super().__init__()
        self.uid = uid


@IndiMessage.register_message
class PingRequest(IndiMessage):
    from_device = True

    def __init__(self, uid: str, **junk):
        super().__init__()
        self.uid = uid
