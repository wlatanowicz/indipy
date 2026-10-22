from indi.message import checks, const
from indi.message.base import IndiMessagePart


class DefIndiMessagePart(IndiMessagePart):
    def __init__(self, name: str, value=None, label: str | None = None, **junk):
        super().__init__(name=name, value=value)
        self.label = label


class DefBLOB(DefIndiMessagePart):
    pass


class DefLight(DefIndiMessagePart):
    def check_value(self, value):
        return checks.dictionary(value, const.State)


class DefNumber(DefIndiMessagePart):
    def __init__(  # noqa: PLR0913
        self,
        name: str,
        format: str | None = "%f",
        min: float | None = 0.0,
        max: float | None = 0.0,
        step: float | None = 0,
        value=None,
        label: str | None = None,
        **junk,
    ):
        super().__init__(name=name, value=value, label=label)
        self.format = "%f" if format is None else format
        self.min = 0.0 if min is None else min
        self.max = 0.0 if max is None else max
        self.step = 0 if step is None else step

    def check_value(self, value):
        return checks.number(value)


class DefSwitch(DefIndiMessagePart):
    def check_value(self, value):
        return checks.dictionary(value, const.SwitchState)


class DefText(DefIndiMessagePart):
    pass
