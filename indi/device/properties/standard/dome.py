from indi.device import properties
from indi.device.properties import const


def DomeSpeed(  # noqa: PLR0913
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
        name="DOME_SPEED",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={"speed": properties.Number(name="DOME_SPEED_VALUE", default=default, min=min, max=max, step=step)},
    )


def DomeMotion(
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="DOME_MOTION",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.AT_MOST_ONE,
        elements={
            "cw": properties.Switch(name="DOME_CW"),
            "ccw": properties.Switch(name="DOME_CCW"),
        },
    )


def DomeTimer(  # noqa: PLR0913
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
        name="DOME_TIMER",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={"timer": properties.Number(name="DOME_TIMER_VALUE", default=default, min=min, max=max, step=step)},
    )


def RelativeDomePosition(  # noqa: PLR0913
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
        name="REL_DOME_POSITION",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "position": properties.Number(
                name="DOME_RELATIVE_POSITION",
                default=default,
                min=min,
                max=max,
                step=step,
            )
        },
    )


def AbsoluteDomePosition(  # noqa: PLR0913
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
        name="ABS_DOME_POSITION",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "position": properties.Number(
                name="DOME_ABSOLUTE_POSITION",
                default=default,
                min=min,
                max=max,
                step=step,
            )
        },
    )


def DomeAbortMotion(
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="DOME_ABORT_MOTION",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.AT_MOST_ONE,
        elements={"abort": properties.Switch(name="ABORT")},
    )


def DomeShutter(
    label=None,
    default="SHUTTER_CLOSE",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="DOME_SHUTTER",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.ONE_OF_MANY,
        elements={
            "open": properties.Switch(name="SHUTTER_OPEN"),
            "close": properties.Switch(name="SHUTTER_CLOSE"),
        },
    )


def DomeGoto(
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="DOME_GOTO",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.AT_MOST_ONE,
        elements={
            "home": properties.Switch(name="DOME_HOME"),
            "park": properties.Switch(name="DOME_PARK"),
        },
    )


def DomeParams(  # noqa: PLR0913
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
        name="DOME_PARAMS",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "home": properties.Number(name="HOME_POSITION", default=default, min=min, max=max, step=step),
            "park": properties.Number(name="PARK_POSITION", default=default, min=min, max=max, step=step),
            "threshold": properties.Number(name="AUTOSYNC_THRESHOLD", default=default, min=min, max=max, step=step),
        },
    )


def DomeAutosync(
    label=None,
    default="DOME_AUTOSYNC_DISABLE",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="DOME_AUTOSYNC",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.ONE_OF_MANY,
        elements={
            "enable": properties.Switch(name="DOME_AUTOSYNC_ENABLE"),
            "disable": properties.Switch(name="DOME_AUTOSYNC_DISABLE"),
        },
    )


def DomeMeasurements(  # noqa: PLR0913
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
        name="DOME_MEASUREMENTS",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "radius": properties.Number(name="DM_DOME_RADIUS", default=default, min=min, max=max, step=step),
            "shutter": properties.Number(name="DOME_SHUTTER_WIDTH", default=default, min=min, max=max, step=step),
            "north": properties.Number(name="DM_NORTH_DISPLACEMENT", default=default, min=min, max=max, step=step),
            "east": properties.Number(name="DM_EAST_DISPLACEMENT", default=default, min=min, max=max, step=step),
            "up": properties.Number(name="DM_UP_DISPLACEMENT", default=default, min=min, max=max, step=step),
            "ota": properties.Number(name="DM_OTA_OFFSET", default=default, min=min, max=max, step=step),
        },
    )


def DomeMeasurementsIndi(  # noqa: PLR0913
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
        name="DOME_MEASUREMENTS",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "radius": properties.Number(name="DM_DOME_RADIUS", default=default, min=min, max=max, step=step),
            "shutter": properties.Number(name="DM_SHUTTER_WIDTH", default=default, min=min, max=max, step=step),
            "north": properties.Number(name="DM_NORTH_DISPLACEMENT", default=default, min=min, max=max, step=step),
            "east": properties.Number(name="DM_EAST_DISPLACEMENT", default=default, min=min, max=max, step=step),
            "up": properties.Number(name="DM_UP_DISPLACEMENT", default=default, min=min, max=max, step=step),
            "ota": properties.Number(name="DM_OTA_OFFSET", default=default, min=min, max=max, step=step),
        },
    )
