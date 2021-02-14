import xml.etree.ElementTree as ET

from indi.message import checks, const


class IndiMessagePart:
    def __init__(self, name, value, **junk):
        self.name = name
        self.value = self.check_value(value)

    def check_value(self, value):
        return value

    @classmethod
    def tag_name(cls):
        return cls.__name__[:1].lower() + cls.__name__[1:]

    @classmethod
    def _all_subclasses(cls):
        return cls.__subclasses__()

    @classmethod
    def from_xml(cls, xml):
        tag = xml.tag
        message_class = None

        for subclass in cls._all_subclasses():
            if subclass.tag_name() == tag:
                message_class = subclass

        if not message_class:
            raise Exception(f"Invalid part: {tag}")

        kwargs = xml.attrib

        kwargs["value"] = xml.text.strip() if xml.text else None

        return message_class(**kwargs)

    def to_xml(self, parent):
        kwargs = {
            k: str(v)
            for k, v in self.__dict__.items()
            if v is not None and k not in ("value",)
        }

        element = ET.SubElement(parent, self.__class__.tag_name(), **kwargs)
        if self.value is not None:
            element.text = str(self.value)

        return element


class DefIndiMessagePart(IndiMessagePart):
    def __init__(self, name, value=None, label=None, **junk):
        super().__init__(name=name, value=value)
        self.label = label


class DefBLOB(DefIndiMessagePart):
    pass


class DefLight(DefIndiMessagePart):
    pass


class DefNumber(DefIndiMessagePart):
    def __init__(self, name, format, min, max, step, value=None, label=None, **junk):
        super().__init__(name=name, value=value, label=label)
        self.format = format
        self.min = min
        self.max = max
        self.step = step


class DefSwitch(DefIndiMessagePart):
    pass


class DefText(DefIndiMessagePart):
    pass


class OneBLOB(IndiMessagePart):
    def __init__(self, name, size, format, value, **junk):
        super().__init__(name=name, value=value)
        self.size = size
        self.format = format


class OneLight(IndiMessagePart):
    def check_value(self, value):
        return checks.dictionary(value, const.State)


class OneNumber(IndiMessagePart):
    pass


class OneSwitch(IndiMessagePart):
    def check_value(self, value):
        return checks.dictionary(value, const.SwitchState)


class OneText(IndiMessagePart):
    pass
