from typing import Optional

from indi.message import IndiMessage


class Device:
    def message_from_client(self, message: IndiMessage):
        raise Exception("Not implemented")

    def accepts(self, device: Optional[str]) -> bool:
        raise Exception("Not implemented")
