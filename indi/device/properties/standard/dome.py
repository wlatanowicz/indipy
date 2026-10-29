from indi.device.properties import const
from indi.device.properties.standard._vector import number_vector, switch_vector

_MEASUREMENTS = (
    ("radius", "DM_DOME_RADIUS"),
    ("north", "DM_NORTH_DISPLACEMENT"),
    ("east", "DM_EAST_DISPLACEMENT"),
    ("up", "DM_UP_DISPLACEMENT"),
    ("ota", "DM_OTA_OFFSET"),
)


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
    return number_vector(
        "DOME_SPEED",
        (("speed", "DOME_SPEED_VALUE"),),
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


def DomeMotion(
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return switch_vector(
        "DOME_MOTION",
        (("cw", "DOME_CW"), ("ccw", "DOME_CCW")),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.AT_MOST_ONE,
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
    return number_vector(
        "DOME_TIMER",
        (("timer", "DOME_TIMER_VALUE"),),
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
    return number_vector(
        "REL_DOME_POSITION",
        (("position", "DOME_RELATIVE_POSITION"),),
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
    return number_vector(
        "ABS_DOME_POSITION",
        (("position", "DOME_ABSOLUTE_POSITION"),),
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


def DomeAbortMotion(
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return switch_vector(
        "DOME_ABORT_MOTION",
        (("abort", "ABORT"),),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.AT_MOST_ONE,
    )


def DomeShutter(
    label=None,
    default="SHUTTER_CLOSE",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return switch_vector(
        "DOME_SHUTTER",
        (("open", "SHUTTER_OPEN"), ("close", "SHUTTER_CLOSE")),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.ONE_OF_MANY,
    )


def DomeGoto(
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return switch_vector(
        "DOME_GOTO",
        (("home", "DOME_HOME"), ("park", "DOME_PARK")),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.AT_MOST_ONE,
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
    return number_vector(
        "DOME_PARAMS",
        (("home", "HOME_POSITION"), ("park", "PARK_POSITION"), ("threshold", "AUTOSYNC_THRESHOLD")),
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


def DomeAutosync(
    label=None,
    default="DOME_AUTOSYNC_DISABLE",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return switch_vector(
        "DOME_AUTOSYNC",
        (("enable", "DOME_AUTOSYNC_ENABLE"), ("disable", "DOME_AUTOSYNC_DISABLE")),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.ONE_OF_MANY,
    )


def _dome_measurements(shutter_name, *, label, default, min, max, step, state, perm, timeout, enabled):  # noqa: PLR0913
    members = (_MEASUREMENTS[0], ("shutter", shutter_name), *_MEASUREMENTS[1:])
    return number_vector(
        "DOME_MEASUREMENTS",
        members,
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
    return _dome_measurements(
        "DOME_SHUTTER_WIDTH",
        label=label,
        default=default,
        min=min,
        max=max,
        step=step,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
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
    return _dome_measurements(
        "DM_SHUTTER_WIDTH",
        label=label,
        default=default,
        min=min,
        max=max,
        step=step,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
    )
