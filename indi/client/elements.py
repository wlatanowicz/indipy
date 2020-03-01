from indi.message import parts


class Element:
    def_message_class = None
    set_message_class = None
    new_message_class = None

    @classmethod
    def from_message(cls, vector, msg):
        for subclass in cls.__subclasses__():
            if isinstance(msg, subclass.def_message_class):
                return subclass(vector, msg)
        return None

    def __init__(self, vector, msg):
        self.name = msg.name
        self.label = msg.label
        self.vector = vector
        self._value = None
        self._new_value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._new_value = value

    def process_message(self, msg):
        if isinstance(msg, self.set_message_class):
            old_value = self.value
            self._value = msg.value
            if self._value != old_value:
                self.vector.device.client.trigger_update(self, "value")

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
