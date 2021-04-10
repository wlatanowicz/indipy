import sys
from functools import reduce

import indi
from indi.device import properties
from indi.device.properties import const


def Connection(
    label=None,
    default="DISCONNECT",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="CONNECTION",
        default_on=default,
        elements=dict(
            connect=properties.Switch(name="CONNECT"),
            disconnect=properties.Switch(name="DISCONNECT"),
        ),
    )


def DriverInfo(name=None, exec=None, version=None, interface=None):
    name = name or "INDIpy Driver"
    exec = exec or sys.argv[0]
    version = version or indi.__version__
    interface = interface or []
    interface = reduce(lambda a, b: a | b, interface, const.DriverInterface.GENERAL)

    elements = {
        "name": properties.TextVector.element_class(name="DRIVER_NAME", default=name),
        "exec": properties.TextVector.element_class(name="DRIVER_EXEC", default=exec),
        "version": properties.TextVector.element_class(
            name="DRIVER_VERSION", default=version
        ),
        "interface": properties.TextVector.element_class(
            name="DRIVER_INTERFACE", default=interface
        ),
    }

    return properties.TextVector(
        "DRIVER_INFO", elements=elements, perm=const.Permissions.READ_ONLY
    )
