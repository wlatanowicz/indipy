import xml.etree.ElementTree as ET

from indi.message import checks, const


class IndiMessagePart:
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
        if hasattr(self, "value") and self.value is not None:
            element.text = str(self.value)

        return element


class DefBLOB(IndiMessagePart):
    def __init__(self, name, label=None, **junk):
        self.name = name
        self.label = label


class DefLight(IndiMessagePart):
    def __init__(self, name, label=None, **junk):
        self.name = name
        self.label = label


class DefNumber(IndiMessagePart):
    def __init__(self, name, format, min, max, step, label=None, **junk):
        self.name = name
        self.format = format
        self.min = min
        self.max = max
        self.step = step
        self.label = label


class DefSwitch(IndiMessagePart):
    def __init__(self, name, label=None, **junk):
        self.name = name
        self.label = label


class DefText(IndiMessagePart):
    def __init__(self, name, label=None, **junk):
        self.name = name
        self.label = label


class OneBLOB(IndiMessagePart):
    def __init__(self, name, size, format, value, **junk):
        self.name = name
        self.size = size
        self.format = format
        self.value = value


class OneLight(IndiMessagePart):
    def __init__(self, name, value, **junk):
        self.name = name
        self.value = checks.dictionary(value, const.State)


class OneNumber(IndiMessagePart):
    def __init__(self, name, value, **junk):
        self.name = name
        self.value = value


class OneSwitch(IndiMessagePart):
    def __init__(self, name, value, **junk):
        self.name = name
        self.value = checks.dictionary(value, const.SwitchState)


class OneText(IndiMessagePart):
    def __init__(self, name, value, **junk):
        self.name = name
        self.value = value
