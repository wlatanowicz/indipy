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
        all_subclasses = []

        for subclass in cls.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(subclass._all_subclasses())

        return set(all_subclasses)

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

    def to_dict(self):
        res = {
            k: str(v)
            for k, v in sorted(self.__dict__.items())
            if v is not None and k not in ("value",)
        }

        if getattr(self, "value", None) is not None:
            res["_value"] = str(self.value)

        return res

    def __eq__(self, other):
        return other.__class__ == self.__class__ and self.to_dict() == other.to_dict()


class DefIndiMessagePart(IndiMessagePart):
    def __init__(self, name, value=None, label=None, **junk):
        super().__init__(name=name, value=value)
        self.label = label


class DefBLOB(DefIndiMessagePart):
    pass


class DefLight(DefIndiMessagePart):
    def check_value(self, value):
        return checks.dictionary(value, const.State)


class DefNumber(DefIndiMessagePart):
    def __init__(self, name, format, min, max, step, value=None, label=None, **junk):
        super().__init__(name=name, value=value, label=label)
        self.format = format
        self.min = min
        self.max = max
        self.step = step

    def check_value(self, value):
        return checks.number(value)


class DefSwitch(DefIndiMessagePart):
    def check_value(self, value):
        return checks.dictionary(value, const.SwitchState)


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
    def check_value(self, value):
        return checks.number(value)


class OneSwitch(IndiMessagePart):
    def check_value(self, value):
        return checks.dictionary(value, const.SwitchState)


class OneText(IndiMessagePart):
    pass
