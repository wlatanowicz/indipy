from __future__ import annotations

from typing import TYPE_CHECKING

from indi.message.base import IndiMessage

if TYPE_CHECKING:
    from indi.message import TimestampType


@IndiMessage.register_message
class DelProperty(IndiMessage):
    from_device = True

    def __init__(
        self,
        device: str,
        name: str | None = None,
        timestamp: TimestampType | None = None,
        message: str | None = None,
        **junk,
    ):
        super().__init__(device)
        self.name = name
        self.timestamp = timestamp
        self.message = message
