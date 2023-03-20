from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple, Type, Union

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
    children_class: Union[
        Type[DefBLOB], Type[DefLight], Type[DefNumber], Type[DefSwitch], Type[DefText]
    ]

    def __init__(
        self,
        device: str,
        name: str,
        state: const.StateType,
        label: Optional[str] = None,
        group: Optional[str] = None,
        timestamp: Optional[TimestampType] = None,
        message: Optional[str] = None,
        children: Optional[Tuple[DefIndiMessagePart, ...]] = None,
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
        timeout: Optional[TimestampType] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.perm = checks.dictionary(perm, const.Permissions)
        self.timeout = timeout


class DefBLOBVector(DefWritableVector):
    children_class = DefBLOB


class DefLightVector(DefVector):
    children_class = DefLight


class DefNumberVector(DefWritableVector):
    children_class = DefNumber


class DefSwitchVector(DefWritableVector):
    children_class = DefSwitch

    def __init__(self, *args, rule: const.SwitchRuleType, **kwargs):
        super().__init__(*args, **kwargs)
        self.rule = checks.dictionary(rule, const.SwitchRule)


class DefTextVector(DefWritableVector):
    children_class = DefText
