from indi.message.base import IndiMessage


class PingReply(IndiMessage):
    from_client = True

    def __init__(self, uid: str, **junk):
        super().__init__()
        self.uid = uid


class PingRequest(IndiMessage):
    from_device = True

    def __init__(self, uid: str, **junk):
        super().__init__()
        self.uid = uid
