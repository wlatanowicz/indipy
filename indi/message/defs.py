from __future__ import annotations

from typing import TYPE_CHECKING

from indi.message import checks, const
from indi.message.base import IndiMessage
from indi.message.def_parts import (
    DefBLOB,
    DefIndiMessagePart,
    DefLight,
    DefNumber,
    DefSwitch,
    DefText,
)

if TYPE_CHECKING:
    from indi.message import TimestampType


class DefVector(IndiMessage):
    from_device = True
    children_class: type[DefBLOB] | type[DefLight] | type[DefNumber] | type[DefSwitch] | type[DefText]

    def __init__(  # noqa: PLR0913
        self,
        device: str,
        name: str,
        state: const.StateType,
        label: str | None = None,
        group: str | None = None,
        timestamp: TimestampType | None = None,
        message: str | None = None,
        children: tuple[DefIndiMessagePart, ...] | None = None,
        **junk,
    ):
        super().__init__(device)
        self.name = name
        self.state = checks.dictionary(state, const.State)
        self.label = label
        self.group = group
        self.timestamp = timestamp
        self.message = message
        self.children = checks.children(children, self.children_class)


class DefWritableVector(DefVector):
    def __init__(
        self,
        *args,
        perm: const.PermissionsType,
        timeout: TimestampType | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.perm = checks.dictionary(perm, const.Permissions)
        self.timeout = timeout


@IndiMessage.register_message
class DefBLOBVector(DefWritableVector):
    children_class = DefBLOB


@IndiMessage.register_message
class DefLightVector(DefVector):
    children_class = DefLight


@IndiMessage.register_message
class DefNumberVector(DefWritableVector):
    children_class = DefNumber


@IndiMessage.register_message
class DefSwitchVector(DefWritableVector):
    children_class = DefSwitch

    def __init__(self, *args, rule: const.SwitchRuleType, **kwargs):
        super().__init__(*args, **kwargs)
        self.rule = checks.dictionary(rule, const.SwitchRule)


@IndiMessage.register_message
class DefTextVector(DefWritableVector):
    children_class = DefText
