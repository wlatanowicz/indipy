from indi.message import parts
from indi.client.events import ValueUpdate
from indi.device import values


class Element:
    def_message_class = None
    set_message_class = None
    new_message_class = None

    @classmethod
    def from_message(cls, vector, msg):
        for subclass in cls.__subclasses__():
            if isinstance(msg, subclass.def_message_class):
                element = subclass(vector, msg)
                event = ValueUpdate(element, None, element._value)
                vector.device.client.trigger_event(event)
                return element
        return None

    def __init__(self, vector, msg):
        self.name = msg.name
        self.label = msg.label
        self.vector = vector
        self._value = msg.value
        self._new_value = None

    @property
    def value(self):
        return self._value

    @property
    def has_new_value(self) -> bool:
        return self._new_value is not None

    def reset_new_value(self):
        self._new_value = None

    @value.setter
    def value(self, value):
        self._new_value = value

    def process_message(self, msg):
        if isinstance(msg, self.set_message_class):
            old_value = self.value
            self.set_value_from_message(msg)
            if self._value != old_value:
                event = ValueUpdate(self, old_value, self._value)
                self.vector.device.client.trigger_event(event)

    def set_value_from_message(self, msg):
        self._value = msg.value

    def to_new_message(self):
        return self.new_message_class(name=self.name, value=self._new_value)


class Number(Element):
    def_message_class = parts.DefNumber
    set_message_class = parts.OneNumber
    new_message_class = parts.OneNumber


class Switch(Element):
    def_message_class = parts.DefSwitch
    set_message_class = parts.OneSwitch
    new_message_class = parts.OneSwitch


class Text(Element):
    def_message_class = parts.DefText
    set_message_class = parts.OneText
    new_message_class = parts.OneText


class Light(Element):
    def_message_class = parts.DefLight
    set_message_class = parts.OneLight
    new_message_class = parts.OneLight


class BLOB(Element):
    def_message_class = parts.DefBLOB
    set_message_class = parts.OneBLOB
    new_message_class = parts.OneBLOB

    def set_value_from_message(self, msg):
        blob_value = values.BLOB.from_base64(msg.value, msg.format)
        assert int(msg.size) == blob_value.size, f"Blob size differs: {msg.size} declared vs {blob_value.size} measured"

        self._value = blob_value
