from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from indi.message.base import IndiMessage

if TYPE_CHECKING:
    from indi.message import TimestampType


class DelProperty(IndiMessage):
    from_device = True

    def __init__(
        self,
        device: str,
        name: Optional[str] = None,
        timestamp: Optional[TimestampType] = None,
        message: Optional[str] = None,
        **junk,
    ):
        super().__init__(device)
        self.name = name
        self.timestamp = timestamp
        self.message = message
