from .IndiMessage import  IndiMessage
from . import checks
from .parts import OneBLOB, OneLight, OneNumber, OneSwitch, OneText
from . import const


class SetVector(IndiMessage):
    child_class = None
    from_device = True

    def __init__(self, device, name, state, timeout=None, timestamp=None, message=None, children=None, **junk):
        self.device = device
        self.name = name
        self.state = checks.dictionary(state, const.State)
        self.timeout = timeout
        self.timestamp = timestamp
        self.message = message
        self.children = checks.children(children, self.child_class)


class SetBLOBVector(SetVector):
    child_class = OneBLOB


class SetLightVector(SetVector):
    child_class = OneLight


class SetNumberVector(SetVector):
    child_class = OneNumber


class SetSwitchVector(SetVector):
    child_class = OneSwitch


class SetTextVector(SetVector):
    child_class = OneText
