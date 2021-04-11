from typing import Optional, Type, Union

from indi.message import checks
from indi.message.base import IndiMessage
from indi.message.one_parts import OneBLOB, OneNumber, OneSwitch, OneText


class NewVector(IndiMessage):
    children_class: Union[
        Type[OneBLOB], Type[OneNumber], Type[OneSwitch], Type[OneText]
    ]
    from_client = True

    def __init__(self, device, name, timestamp=None, children=None, **junk):
        self.device = device
        self.name = name
        self.timestamp = timestamp
        self.children = checks.children(children, self.children_class)


class NewBLOBVector(NewVector):
    children_class = OneBLOB


class NewNumberVector(NewVector):
    children_class = OneNumber


class NewSwitchVector(NewVector):
    children_class = OneSwitch


class NewTextVector(NewVector):
    children_class = OneText
