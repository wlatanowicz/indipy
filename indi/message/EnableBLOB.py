from .IndiMessage import IndiMessage
from . import checks
from . import const


class EnableBLOB(IndiMessage):
    from_client = True

    def __init__(self, device, value, name=None, **junk):
        self.device = device
        self.name = name
        self.value = checks.dictionary(value, const.BLOBEnable)
