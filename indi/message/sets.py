from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple, Type, Union

from indi.message import checks, const
from indi.message.base import IndiMessage
from indi.message.one_parts import (
    IndiMessagePart,
    OneBLOB,
    OneLight,
    OneNumber,
    OneSwitch,
    OneText,
)

if TYPE_CHECKING:
    from indi.message import TimestampType


class SetVector(IndiMessage):
    child_class: Union[
        Type[OneBLOB], Type[OneLight], Type[OneNumber], Type[OneSwitch], Type[OneText]
    ]
    from_device = True

    def __init__(
        self,
        device: str,
        name: str,
        state: const.StateType,
        timeout: Optional[float] = None,
        timestamp: Optional[TimestampType] = None,
        message: Optional[str] = None,
        children: Optional[Tuple[IndiMessagePart, ...]] = None,
        **junk,
    ):
        super().__init__(device)
        self.name = name
        self.state = checks.dictionary(state, const.State)
        self.timeout = timeout
        self.timestamp = timestamp
        self.message = message
        self.children = checks.children(children, self.child_class)


class SetBLOBVector(SetVector):
    child_class = OneBLOB


class SetLightVector(SetVector):
    child_class = OneLight


class SetNumberVector(SetVector):
    child_class = OneNumber


class SetSwitchVector(SetVector):
    child_class = OneSwitch


class SetTextVector(SetVector):
    child_class = OneText
