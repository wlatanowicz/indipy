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
    return properties.TextVector(
        name="DEVICE_PORT",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={"port": properties.Text(name="PORT", default=default)},
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
    return properties.NumberVector(
        name="TIME_LST",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={"lst": properties.Number(name="LST", default=default, min=min, max=max, step=step)},
    )


def TimeUtc(
    label=None,
    default="",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.TextVector(
        name="TIME_UTC",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "utc": properties.Text(name="UTC", default=default),
            "offset": properties.Text(name="OFFSET", default=default),
        },
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
    return properties.NumberVector(
        name="GEOGRAPHIC_COORD",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "lat": properties.Number(name="LAT", default=default, min=min, max=max, step=step),
            "long": properties.Number(name="LONG", default=default, min=min, max=max, step=step),
            "elev": properties.Number(name="ELEV", default=default, min=min, max=max, step=step),
        },
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
    return properties.NumberVector(
        name="ATMOSPHERE",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "temperature": properties.Number(name="TEMPERATURE", default=default, min=min, max=max, step=step),
            "pressure": properties.Number(name="PRESSURE", default=default, min=min, max=max, step=step),
            "humidity": properties.Number(name="HUMIDITY", default=default, min=min, max=max, step=step),
        },
    )


def UploadSettings(
    label=None,
    default="",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.TextVector(
        name="UPLOAD_SETTINGS",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "directory": properties.Text(name="UPLOAD_DIR", default=default),
            "prefix": properties.Text(name="UPLOAD_PREFIX", default=default),
        },
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
    return properties.TextVector(
        name="ACTIVE_DEVICES",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={_ACTIVE_DEVICE_MEMBERS[member]: properties.Text(name=member, default=default) for member in members},
    )
