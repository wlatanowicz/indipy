from __future__ import annotations

import xml.etree.cElementTree as ET
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Type

if TYPE_CHECKING:
    from indi.message import TimestampType


class IndiMessage:
    from_device = False
    from_client = False

    _message_classes: List[Type[IndiMessage]] = []

    def __init__(self, device=None, **junk):
        self.device = device

    @classmethod
    def tag_name(cls):
        return cls.__name__[:1].lower() + cls.__name__[1:]

    @classmethod
    def register_message(cls, message_class):
        cls._message_classes.append(message_class)
        return message_class

    @classmethod
    def all_message_classes(cls):
        return cls._message_classes

    @classmethod
    def from_xml(cls, xml: ET.Element) -> IndiMessage:
        tag = xml.tag
        message_class = None

        for subclass in cls.all_message_classes():
            if subclass.tag_name() == tag:
                message_class = subclass

        if not message_class:
            raise Exception(f"Invalid message: {tag}")

        kwargs: Dict[str, Any] = xml.attrib

        children: Tuple[ET.Element, ...] = tuple(
            IndiMessagePart.from_xml(child) for child in xml
        )
        if children:
            kwargs["children"] = children

        if xml.text:
            kwargs["value"] = xml.text.strip()

        return message_class(**kwargs)

    @classmethod
    def from_string(cls, string: str) -> IndiMessage:
        xml = ET.fromstring(string)
        return cls.from_xml(xml)

    def to_xml(self):
        kwargs = {
            k: str(v)
            for k, v in sorted(self.__dict__.items())
            if v is not None
            and k
            not in (
                "children",
                "value",
            )
        }

        element = ET.Element(self.__class__.tag_name(), **kwargs)

        if getattr(self, "value", None) is not None:
            element.text = str(self.value)

        if hasattr(self, "children"):
            for child in self.children:
                child.to_xml(element)

        return element

    def to_string(self) -> bytes:
        xml = self.to_xml()
        return b'<?xml version="1.0"?>\n' + ET.tostring(xml) + b"\n"

    def to_dict(self):
        res = {
            k: str(v)
            for k, v in sorted(self.__dict__.items())
            if v is not None
            and k
            not in (
                "children",
                "value",
            )
        }

        if getattr(self, "value", None) is not None:
            res["_value"] = str(self.value)

        if hasattr(self, "children"):
            for child in self.children:
                res["_children"] = child.to_dict()

        return res

    def __eq__(self, other):
        return other.__class__ == self.__class__ and self.to_dict() == other.to_dict()


class Message(IndiMessage):
    from_device = True

    def __init__(
        self,
        device: Optional[str] = None,
        timestamp: Optional[TimestampType] = None,
        message: Optional[str] = None,
        **junk,
    ):
        super().__init__(device)
        self.timestamp = timestamp
        self.message = message


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
