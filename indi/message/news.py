from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple, Type, Union

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
    children_class: Union[
        Type[OneBLOB], Type[OneNumber], Type[OneSwitch], Type[OneText]
    ]
    from_client = True

    def __init__(
        self,
        device: str,
        name: str,
        timestamp: Optional[TimestampType] = None,
        children: Optional[Tuple[IndiMessagePart, ...]] = None,
        **junk,
    ):
        super().__init__(device)
        self.name = name
        self.timestamp = timestamp
        self.children = checks.children(children, self.children_class)


class NewBLOBVector(NewVector):
    children_class = OneBLOB


class NewNumberVector(NewVector):
    children_class = OneNumber


class NewSwitchVector(NewVector):
    children_class = OneSwitch


class NewTextVector(NewVector):
    children_class = OneText
