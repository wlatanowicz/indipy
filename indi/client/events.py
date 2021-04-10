from __future__ import annotations

from typing import TYPE_CHECKING

from indi.message.const import State, SwitchState

if TYPE_CHECKING:
    from indi.client.device import Device
    from indi.client.elements import Element
    from indi.client.vectors import Vector


class BaseEvent:
    def __init__(
        self, device: Device = None, vector: Vector = None, element: Element = None
    ):
        self.device = device
        self.vector = vector
        self.element = element

    def __str__(self):
        res = f"Event <{self.__class__.__name__}>:"
        props = (
            "device",
            "vector",
            "element",
        )
        for prop in props:
            obj = getattr(self, prop)
            if obj:
                res += f" {prop}={obj.name}"
        return res


class DefinitionUpdate(BaseEvent):
    def __init__(self, vector: Vector):
        super().__init__(device=vector.device, vector=vector)


class ValueUpdate(BaseEvent):
    def __init__(self, element: Element, old_value, new_value):
        super().__init__(
            device=element.vector.device, vector=element.vector, element=element
        )
        self.old_value = old_value
        self.new_value = new_value

    def __str__(self):
        from indi.client import elements

        old_value = str(self.old_value) if self.old_value is not None else "∅"
        new_value = str(self.new_value) if self.new_value is not None else "∅"

        if isinstance(self.element, elements.Switch):
            switch_icons = {
                None: "∅",
                SwitchState.ON: "🌕",
                SwitchState.OFF: "🌑",
            }
            old_value = switch_icons[self.old_value]
            new_value = switch_icons[self.new_value]

        if isinstance(self.element, elements.Light):
            light_icons = {
                None: "∅",
                State.IDLE: "⚪️",
                State.OK: "🟢",
                State.BUSY: "🟡",
                State.ALERT: "🔴",
            }
            old_value = light_icons[self.old_value]
            new_value = light_icons[self.new_value]

        old_value = "\033[1m" + old_value + "\033[0m"
        new_value = "\033[1m" + new_value + "\033[0m"
        return super().__str__() + f" {old_value} → {new_value}"


class StateUpdate(BaseEvent):
    def __init__(self, vector: Vector, old_state, new_state):
        super().__init__(device=vector.device, vector=vector)
        self.old_state = old_state
        self.new_state = new_state

    def __str__(self):
        state_icons = {
            None: "∅",
            State.IDLE: "⚪️",
            State.OK: "🟢",
            State.BUSY: "🟡",
            State.ALERT: "🔴",
        }
        return (
            super().__str__()
            + f" {state_icons[self.old_state]} → {state_icons[self.new_state]}"
        )
