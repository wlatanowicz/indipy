import xml.etree.ElementTree as ET

from indi.message import checks, const
from indi.message.base import IndiMessage, IndiMessagePart


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
