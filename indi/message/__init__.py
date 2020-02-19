import datetime

from .defs import (DefBLOBVector, DefLightVector, DefNumberVector,
                   DefSwitchVector, DefTextVector, DefVector)
from .DelProperty import DelProperty
from .EnableBLOB import EnableBLOB
from .GetProperties import GetProperties
from .IndiMessage import IndiMessage
from .Message import Message
from .news import (NewBLOBVector, NewNumberVector, NewSwitchVector,
                   NewTextVector, NewVector)
from .sets import (SetBLOBVector, SetLightVector, SetNumberVector,
                   SetSwitchVector, SetTextVector, SetVector)


def now():
    return datetime.datetime.utcnow().isoformat()
