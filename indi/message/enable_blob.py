from indi.message import checks, const
from indi.message.base import IndiMessage


@IndiMessage.register_message
class EnableBLOB(IndiMessage):
    from_client = True

    def __init__(self, device: str, value: const.BLOBEnableType, name: str | None = None, **junk):
        super().__init__(device)
        self.name = name
        self.value = checks.dictionary(value, const.BLOBEnable)
