import datetime

from .base import IndiMessage, Message
from .defs import (
    DefBLOBVector,
    DefLightVector,
    DefNumberVector,
    DefSwitchVector,
    DefTextVector,
    DefVector,
)
from .del_property import DelProperty
from .enable_blob import EnableBLOB
from .get_properties import GetProperties
from .news import (
    NewBLOBVector,
    NewNumberVector,
    NewSwitchVector,
    NewTextVector,
    NewVector,
)
from .one_light import OneLight
from .sets import (
    SetBLOBVector,
    SetLightVector,
    SetNumberVector,
    SetSwitchVector,
    SetTextVector,
    SetVector,
)


def now():
    return datetime.datetime.utcnow().isoformat()
