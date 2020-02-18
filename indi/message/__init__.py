import datetime

from .IndiMessage import IndiMessage

from .GetProperties import GetProperties
from .DelProperty import DelProperty
from .EnableBLOB import EnableBLOB

from .defs import (
    DefVector,
    DefBLOBVector,
    DefLightVector,
    DefNumberVector,
    DefSwitchVector,
    DefTextVector,
)
from .sets import (
    SetVector,
    SetBLOBVector,
    SetLightVector,
    SetNumberVector,
    SetSwitchVector,
    SetTextVector,
)
from .news import (
    NewVector,
    NewBLOBVector,
    NewNumberVector,
    NewSwitchVector,
    NewTextVector,
)

from .Message import Message


def now():
    return datetime.datetime.utcnow().isoformat()
