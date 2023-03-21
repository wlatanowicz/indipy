from typing import Optional

from indi.message import checks, const
from indi.message.base import IndiMessagePart


class DefIndiMessagePart(IndiMessagePart):
    def __init__(self, name: str, value=None, label: Optional[str] = None, **junk):
        super().__init__(name=name, value=value)
        self.label = label


class DefBLOB(DefIndiMessagePart):
    pass


class DefLight(DefIndiMessagePart):
    def check_value(self, value):
        return checks.dictionary(value, const.State)


class DefNumber(DefIndiMessagePart):
    def __init__(
        self,
        name: str,
        format,
        min: float,
        max: float,
        step: float,
        value=None,
        label: Optional[str] = None,
        **junk
    ):
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
