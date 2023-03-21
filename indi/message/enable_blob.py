from typing import Optional

from indi.message import checks, const
from indi.message.base import IndiMessage


class EnableBLOB(IndiMessage):
    from_client = True

    def __init__(
        self,
        device: str,
        value: const.BLOBEnableType,
        name: Optional[str] = None,
        **junk
    ):
        super().__init__(device)
        self.name = name
        self.value = checks.dictionary(value, const.BLOBEnable)
