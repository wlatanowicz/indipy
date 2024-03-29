from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Tuple, Type, Union, cast

from indi import message
from indi.device.properties.instance.elements import Element, Switch
from indi.message import checks, const

if TYPE_CHECKING:
    from indi.device.driver import Driver
    from indi.device.properties.definition.vectors import Vector as VectorDefinition
    from indi.device.properties.instance.elements import Switch
    from indi.device.properties.instance.group import Group


class Vector:
    def_message_class: Type[message.DefVector]
    set_message_class: Union[
        Type[message.SetBLOBVector],
        Type[message.SetLightVector],
        Type[message.SetNumberVector],
        Type[message.SetSwitchVector],
        Type[message.SetTextVector],
    ]
    new_message_class: Union[
        Type[message.NewBLOBVector],
        Type[message.NewNumberVector],
        Type[message.NewSwitchVector],
        Type[message.NewTextVector],
    ]

    def __init__(self, group: Group, definition: VectorDefinition) -> None:
        self._state = definition.state
        self._enabled = definition.enabled
        self._group = group
        self._definition = definition
        self._elements: Dict[str, Element] = {
            k: v.instance(self) for k, v in definition.elements.items()
        }
        self._elements_by_name: Dict[str, Element] = {
            v.name: v for k, v in self._elements.items()
        }

    def __getattr__(self, item: str):
        element = self._elements.get(item)
        if element:
            return element

        return self.__getattribute__(item)

    @property
    def device(self) -> Driver:
        return self._group.device

    @property
    def group(self) -> Group:
        return self._group

    @property
    def name(self) -> str:
        return self._definition.name

    @property
    def enabled(self) -> bool:
        return self._enabled and self.group.enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value
        self.device.send_message(self.to_def_message())
        self.device.send_message(self.to_set_message())

    @property
    def state_(self) -> const.StateType:
        return self._state

    @state_.setter
    def state_(self, value: const.StateType):
        self._state = checks.dictionary(value, const.State)
        self.device.send_message(self.to_set_message())

    def to_def_message(self) -> Union[message.DefVector, message.DelProperty]:
        if not self.enabled:
            return message.DelProperty(
                device=self.device.name,
                name=self._definition.name,
                timestamp=message.now(),
            )

        elements = tuple(
            e.to_def_message() for k, e in self._elements.items() if e.enabled
        )
        return self.def_message_class(
            device=self.device.name,
            name=self._definition.name,
            group=self._group.name,
            label=self._definition.label,
            state=self._state,
            perm=self._definition.perm,
            timeout=self._definition.timeout,
            timestamp=message.now(),
            children=elements,
        )

    def to_set_message(self) -> Optional[message.SetVector]:
        if not self.enabled:
            return None

        elements = tuple(
            e.to_set_message() for k, e in self._elements.items() if e.enabled
        )
        return self.set_message_class(
            device=self.device.name,
            name=self._definition.name,
            state=self._state,
            timeout=self._definition.timeout,
            timestamp=message.now(),
            children=elements,
        )

    def from_new_message(self, msg: message.NewVector):
        for child in msg.children:
            self._elements_by_name[child.name].set_value_from_message(child)


class NumberVector(Vector):
    def_message_class = message.DefNumberVector
    set_message_class = message.SetNumberVector
    new_message_class = message.NewNumberVector


class TextVector(Vector):
    def_message_class = message.DefTextVector
    set_message_class = message.SetTextVector
    new_message_class = message.NewTextVector


class SwitchVector(Vector):
    def_message_class = message.DefSwitchVector
    set_message_class = message.SetSwitchVector
    new_message_class = message.NewSwitchVector

    @property
    def selected_value(self):
        res = self.selected_values
        if len(res) > 1:
            raise Exception("Multiple values selected")

        try:
            return res[0]
        except IndexError:
            return None

    @selected_value.setter
    def selected_value(self, value):
        self.selected_values = [value]

    @property
    def selected_values(self) -> Tuple[str, ...]:
        elements = cast(Dict[str, Switch], self._elements)
        return tuple(el.name for el in elements.values() if el.bool_value)

    @selected_values.setter
    def selected_values(self, values):
        for v in values:
            if v not in self._elements_by_name:
                raise Exception(f"Vector {self.name} does not have element {v}")

        elements = cast(Dict[str, Switch], self._elements)
        for k, el in elements:
            new_value = el.name in values
            if el.bool_value != new_value:
                el.bool_value = new_value

    def reset_selected_value(self, value):
        self.reset_selected_values([value])

    def reset_selected_values(self, values):
        for v in values:
            if v not in self._elements_by_name:
                raise Exception()

        for k, el in self._elements.items():
            el.reset_bool_value(el.name in values)

    def apply_rule(self, sender: Switch, new_value):
        if new_value == const.SwitchState.ON:
            if self._definition.rule in (
                const.SwitchRule.AT_MOST_ONE,
                const.SwitchRule.ONE_OF_MANY,
            ):
                for k, el in self._elements.items():
                    if el != sender and el._value == const.SwitchState.ON:
                        el._value = const.SwitchState.OFF
        else:
            if self._definition.rule in (const.SwitchRule.ONE_OF_MANY,):
                if (
                    len(
                        [
                            el
                            for k, el in self._elements.items()
                            if el != sender and el._value == const.SwitchState.ON
                        ]
                    )
                    <= 0
                ):
                    new_value = const.SwitchState.ON

        return new_value

    def to_def_message(self) -> Union[message.DefVector, message.DelProperty]:
        if not self.enabled:
            return message.DelProperty(
                device=self.device.name,
                name=self._definition.name,
                timestamp=message.now(),
            )

        elements = [e.to_def_message() for k, e in self._elements.items() if e.enabled]
        return self.def_message_class(
            device=self.device.name,
            name=self._definition.name,
            group=self._group.name,
            label=self._definition.label,
            state=self._state,
            perm=self._definition.perm,
            rule=self._definition.rule,
            timeout=self._definition.timeout,
            timestamp=message.now(),
            children=elements,
        )


class LightVector(Vector):
    def_message_class = message.DefLightVector
    set_message_class = message.SetLightVector

    def to_def_message(self):
        if not self.enabled:
            return message.DelProperty(
                device=self.device.name,
                name=self._definition.name,
                timestamp=message.now(),
            )

        elements = [e.to_def_message() for k, e in self._elements.items() if e.enabled]
        return self.def_message_class(
            device=self.device.name,
            name=self._definition.name,
            group=self.group.name,
            label=self._definition.label,
            state=self._state,
            timestamp=message.now(),
            children=elements,
        )

    def to_set_message(self):
        if not self.enabled:
            return None

        elements = [e.to_set_message() for k, e in self._elements.items() if e.enabled]
        return self.set_message_class(
            device=self.device.name,
            name=self._definition.name,
            state=self._state,
            timestamp=message.now(),
            children=elements,
        )


class BLOBVector(Vector):
    def_message_class = message.DefBLOBVector
    set_message_class = message.SetBLOBVector
    new_message_class = message.NewBLOBVector
