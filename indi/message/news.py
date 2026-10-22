from __future__ import annotations

from typing import TYPE_CHECKING

from indi.message import checks
from indi.message.base import IndiMessage
from indi.message.one_parts import (
    IndiMessagePart,
    OneBLOB,
    OneNumber,
    OneSwitch,
    OneText,
)

if TYPE_CHECKING:
    from indi.message import TimestampType


class NewVector(IndiMessage):
    children_class: type[OneBLOB] | type[OneNumber] | type[OneSwitch] | type[OneText]
    from_client = True

    def __init__(
        self,
        device: str,
        name: str,
        timestamp: TimestampType | None = None,
        children: tuple[IndiMessagePart, ...] | None = None,
        **junk,
    ):
        super().__init__(device)
        self.name = name
        self.timestamp = timestamp
        self.children = checks.children(children, self.children_class)


@IndiMessage.register_message
class NewBLOBVector(NewVector):
    children_class = OneBLOB


@IndiMessage.register_message
class NewNumberVector(NewVector):
    children_class = OneNumber


@IndiMessage.register_message
class NewSwitchVector(NewVector):
    children_class = OneSwitch


@IndiMessage.register_message
class NewTextVector(NewVector):
    children_class = OneText
