import datetime
from typing import NewType

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
from .pings import PingReply, PingRequest
from .sets import (
    SetBLOBVector,
    SetLightVector,
    SetNumberVector,
    SetSwitchVector,
    SetTextVector,
    SetVector,
)

TimestampType = NewType("TimestampType", str)


def now() -> TimestampType:
    moment = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
    return TimestampType(moment.isoformat())


__all__ = [
    "DefBLOBVector",
    "DefLightVector",
    "DefNumberVector",
    "DefSwitchVector",
    "DefTextVector",
    "DefVector",
    "DelProperty",
    "EnableBLOB",
    "GetProperties",
    "IndiMessage",
    "Message",
    "NewBLOBVector",
    "NewNumberVector",
    "NewSwitchVector",
    "NewTextVector",
    "NewVector",
    "OneLight",
    "PingReply",
    "PingRequest",
    "SetBLOBVector",
    "SetLightVector",
    "SetNumberVector",
    "SetSwitchVector",
    "SetTextVector",
    "SetVector",
    "TimestampType",
    "now",
]
