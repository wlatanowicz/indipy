from __future__ import annotations

from typing import TYPE_CHECKING

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
    child_class: type[OneBLOB] | type[OneLight] | type[OneNumber] | type[OneSwitch] | type[OneText]
    from_device = True

    def __init__(  # noqa: PLR0913
        self,
        device: str,
        name: str,
        state: const.StateType,
        timeout: float | None = None,
        timestamp: TimestampType | None = None,
        message: str | None = None,
        children: tuple[IndiMessagePart, ...] | None = None,
        **junk,
    ):
        super().__init__(device)
        self.name = name
        self.state = checks.dictionary(state, const.State)
        self.timeout = timeout
        self.timestamp = timestamp
        self.message = message
        self.children = checks.children(children, self.child_class)


@IndiMessage.register_message
class SetBLOBVector(SetVector):
    child_class = OneBLOB


@IndiMessage.register_message
class SetLightVector(SetVector):
    child_class = OneLight


@IndiMessage.register_message
class SetNumberVector(SetVector):
    child_class = OneNumber


@IndiMessage.register_message
class SetSwitchVector(SetVector):
    child_class = OneSwitch


@IndiMessage.register_message
class SetTextVector(SetVector):
    child_class = OneText
