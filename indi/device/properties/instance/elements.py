import base64
import logging
from typing import Type, Union

from indi.device.properties.instance.vectors import Vector
from indi.message import checks, const, parts


class Element:
    def_message_class: Union[Type[parts.DefSwitch], Type[parts.DefNumber], Type[parts.DefLight], Type[parts.DefBLOB], Type[parts.DefText]]
    set_message_class: Union[Type[parts.OneSwitch], Type[parts.OneNumber], Type[parts.OneLight], Type[parts.OneBLOB], Type[parts.OneText]]

    def __init__(self, vector: Vector, definition):
        self._vector = vector
        self._definition = definition
        self._value = definition.default
        self._enabled = definition.enabled

    @property
    def name(self):
        return self._definition.name

    @property
    def device(self):
        return self._vector.device

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @property
    def value(self):
        self.device.trigger_callback(self._definition.onread, self)
        return self._value

    @value.setter
    def value(self, value):
        logging.debug(
            f"Element: setting value of element {self._definition.name} to {value}"
        )
        prev_value = self._value
        self._value = self.check_value(value)
        self.device.send_message(self._vector.to_set_message())

        if prev_value != self._value:
            self.device.trigger_callback(self._definition.onchange, self)
            self.device.trigger_callback(self._vector.onchange, self._vector)
            self.device.trigger_callback(
                self._vector.group.onchange, self._vector.group
            )
            self.device.trigger_callback(self.device.onchange, self.device)

    def set_value(self, value):
        if self._definition.onwrite is not None:
            self.device.trigger_callback(self._definition.onwrite, self, value=value)
        else:
            self.value = value

    def reset_value(self, value):
        self._value = self.check_value(value)

    def check_value(self, value):
        return value

    def to_def_message(self):
        return self.def_message_class(
            name=self._definition.name, value=self.value, label=self._definition.label,
        )

    def to_set_message(self):
        return self.set_message_class(name=self._definition.name, value=self.value)


class Number(Element):
    def_message_class = parts.DefNumber
    set_message_class = parts.OneNumber

    def to_def_message(self):
        return self.def_message_class(
            name=self._definition.name,
            value=self.value,
            label=self._definition.label,
            format=self._definition.format,
            min=self._definition.min,
            max=self._definition.max,
            step=self._definition.step,
        )


class Text(Element):
    def_message_class = parts.DefText
    set_message_class = parts.OneText


class Switch(Element):
    def_message_class = parts.DefSwitch
    set_message_class = parts.OneSwitch

    def check_value(self, value):
        value = checks.dictionary(value, const.SwitchState)
        return self._vector.apply_rule(self, value)

    @property
    def bool_value(self):
        return self.value == const.SwitchState.ON

    @bool_value.setter
    def bool_value(self, value):
        self.value = const.SwitchState.ON if value else const.SwitchState.OFF

    def reset_bool_value(self, value):
        self._value = const.SwitchState.ON if value else const.SwitchState.OFF


class Light(Element):
    def_message_class = parts.DefLight
    set_message_class = parts.OneLight

    def check_value(self, value):
        return checks.dictionary(value, const.State)


class BLOB(Element):
    def_message_class = parts.DefBLOB
    set_message_class = parts.OneBLOB

    @property
    def bin_value(self):
        return base64.b64decode(self.value)

    @bin_value.setter
    def bin_value(self, value):
        self.value = base64.b64encode(value)
