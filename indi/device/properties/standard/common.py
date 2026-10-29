import sys
from functools import reduce

import indi
from indi.device import properties
from indi.device.properties import const
from indi.device.properties.standard._vector import number_vector, text_vector


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
        elements={
            "connect": properties.Switch(name="CONNECT"),
            "disconnect": properties.Switch(name="DISCONNECT"),
        },
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
        "version": properties.TextVector.element_class(name="DRIVER_VERSION", default=version),
        "interface": properties.TextVector.element_class(name="DRIVER_INTERFACE", default=interface),
    }

    return properties.TextVector("DRIVER_INFO", elements=elements, perm=const.Permissions.READ_ONLY)


_ACTIVE_DEVICE_MEMBERS = {
    "ACTIVE_TELESCOPE": "telescope",
    "ACTIVE_CCD": "ccd",
    "ACTIVE_FILTER": "filter",
    "ACTIVE_FOCUSER": "focuser",
    "ACTIVE_DOME": "dome",
    "ACTIVE_GPS": "gps",
}


def DevicePort(
    label=None,
    default="",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return text_vector(
        "DEVICE_PORT",
        (("port", "PORT"),),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
    )


def TimeLst(  # noqa: PLR0913
    label=None,
    default=0,
    min=0,
    max=0,
    step=0,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return number_vector(
        "TIME_LST",
        (("lst", "LST"),),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        min=min,
        max=max,
        step=step,
    )


def TimeUtc(
    label=None,
    default="",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return text_vector(
        "TIME_UTC",
        (("utc", "UTC"), ("offset", "OFFSET")),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
    )


def GeographicCoord(  # noqa: PLR0913
    label=None,
    default=0,
    min=0,
    max=0,
    step=0,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return number_vector(
        "GEOGRAPHIC_COORD",
        (("lat", "LAT"), ("long", "LONG"), ("elev", "ELEV")),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        min=min,
        max=max,
        step=step,
    )


def Atmosphere(  # noqa: PLR0913
    label=None,
    default=0,
    min=0,
    max=0,
    step=0,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return number_vector(
        "ATMOSPHERE",
        (("temperature", "TEMPERATURE"), ("pressure", "PRESSURE"), ("humidity", "HUMIDITY")),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        min=min,
        max=max,
        step=step,
    )


def UploadSettings(
    label=None,
    default="",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return text_vector(
        "UPLOAD_SETTINGS",
        (("directory", "UPLOAD_DIR"), ("prefix", "UPLOAD_PREFIX")),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
    )


def ActiveDevices(
    *members,
    label=None,
    default="",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    if not members:
        raise ValueError("ACTIVE_DEVICES requires at least one member")
    unknown = [member for member in members if member not in _ACTIVE_DEVICE_MEMBERS]
    if unknown:
        raise ValueError(f"Unknown ACTIVE_DEVICES member: {', '.join(unknown)}")
    elements = tuple((_ACTIVE_DEVICE_MEMBERS[member], member) for member in members)
    return text_vector(
        "ACTIVE_DEVICES",
        elements,
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
    )
