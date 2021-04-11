import base64
import logging
from typing import Type, Union

from indi.device import events, values
from indi.device.events import EventSource
from indi.device.properties.instance.vectors import Vector
from indi.message import checks, const, def_parts, one_parts


class Element(EventSource):
    def_message_class: Union[
        Type[def_parts.DefSwitch],
        Type[def_parts.DefNumber],
        Type[def_parts.DefLight],
        Type[def_parts.DefBLOB],
        Type[def_parts.DefText],
    ]
    set_message_class: Union[
        Type[one_parts.OneSwitch],
        Type[one_parts.OneNumber],
        Type[one_parts.OneLight],
        Type[one_parts.OneBLOB],
        Type[one_parts.OneText],
    ]
    allowed_value_types = (None.__class__,)

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
    def vector(self):
        return self._vector

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @property
    def value(self):
        e = events.Read(element=self)
        self.raise_event(e)
        return self._value

    @value.setter
    def value(self, value):
        logging.debug(
            f"Element: setting value of element {self._definition.name} to {value}"
        )
        prev_value = self._value
        self.check_value_type(value)
        self._value = self.check_value(value)
        self.device.send_message(self._vector.to_set_message())

        if prev_value != self._value:
            e = events.Change(element=self, old_value=prev_value, new_value=self._value)
            self.raise_event(e)

    def set_value(self, value):
        e = events.Write(element=self, new_value=value)
        self.raise_event(e)

        if not e.prevent_default:
            self.value = value

    def set_value_from_message(self, msg):
        self.set_value(msg.value)

    def reset_value(self, value):
        self._value = self.check_value(value)

    def check_value(self, value):
        return value

    def check_value_type(self, value):
        assert isinstance(
            value, self.allowed_value_types
        ), f"Value of {self.name} should be of type {self.allowed_value_types}"

    def to_def_message(self):
        return self.def_message_class(
            name=self._definition.name,
            value=self.value,
            label=self._definition.label,
        )

    def to_set_message(self):
        return self.set_message_class(name=self._definition.name, value=self.value)


class Number(Element):
    def_message_class = def_parts.DefNumber
    set_message_class = one_parts.OneNumber
    allowed_value_types = (
        int,
        float,
    ) + Element.allowed_value_types

    def to_def_message(self):
        return self.def_message_class(
            name=self._definition.name,
            value=values.num_to_str(self.value, self._definition.format),
            label=self._definition.label,
            format=self._definition.format,
            min=self._definition.min,
            max=self._definition.max,
            step=self._definition.step,
        )

    def to_set_message(self):
        return self.set_message_class(
            name=self._definition.name,
            value=values.num_to_str(self.value, self._definition.format),
        )

    def set_value_from_message(self, msg):
        self.set_value(values.str_to_num(msg.value, self._definition.format))


class Text(Element):
    def_message_class = def_parts.DefText
    set_message_class = one_parts.OneText
    allowed_value_types = (str,) + Element.allowed_value_types


class Switch(Element):
    def_message_class = def_parts.DefSwitch
    set_message_class = one_parts.OneSwitch
    allowed_value_types = (str,) + Element.allowed_value_types

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
    def_message_class = def_parts.DefLight
    set_message_class = one_parts.OneLight
    allowed_value_types = (str,) + Element.allowed_value_types

    def check_value(self, value):
        return checks.dictionary(value, const.State)


class BLOB(Element):
    def_message_class = def_parts.DefBLOB
    set_message_class = one_parts.OneBLOB
    allowed_value_types = (values.BLOB,) + Element.allowed_value_types

    def to_set_message(self):
        if self.value is None:
            return self.set_message_class(
                name=self._definition.name, value=None, format=None, size=None
            )
        return self.set_message_class(
            name=self._definition.name,
            value=self.value.binary_base64,
            format=self.value.format,
            size=self.value.size,
        )

    def set_value_from_message(self, msg):
        blob_value = values.BLOB.from_base64(msg.value, msg.format)
        assert msg.size == blob_value.size
        self.set_value(blob_value)
