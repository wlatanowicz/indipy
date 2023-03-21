from typing import Optional

from indi.message.base import IndiMessage


class GetProperties(IndiMessage):
    from_device = True
    from_client = True

    def __init__(
        self,
        version: str,
        device: Optional[str] = None,
        name: Optional[str] = None,
        **junk
    ):
        super().__init__(device)
        self.version = version
        self.name = name
