from indi.device import properties
from indi.device.properties import const
from indi.device.properties.standard._vector import number_vector, switch_vector


def AbsolutePosition(  # noqa: PLR0913
    label=None,
    default=0,
    min=0,
    max=1000,
    step=1,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.NumberVector(
        name="ABS_FOCUS_POSITION",
        elements={
            "position": properties.Number(
                name="FOCUS_ABSOLUTE_POSITION",
                default=default,
                min=min,
                max=max,
                step=step,
            )
        },
    )


def RelativePosition(  # noqa: PLR0913
    label=None,
    min=1,
    max=1000,
    step=1,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.NumberVector(
        name="REL_FOCUS_POSITION",
        elements={"position": properties.Number(name="FOCUS_RELATIVE_POSITION", min=min, max=max, step=step)},
    )


def FocusMax(
    label=None,
    default=1000,
    state=const.State.OK,
    perm=const.Permissions.READ_ONLY,
    timeout=0,
    enabled=True,
):
    return properties.NumberVector(
        name="FOCUS_MAX",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={"max": properties.Number(name="FOCUS_MAX_VALUE", default=default)},
    )


def FocusMotion(
    label=None,
    default="FOCUS_INWARD",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="FOCUS_MOTION",
        default_on=default,
        rule=const.SwitchRule.ONE_OF_MANY,
        elements={
            "inward": properties.Switch(name="FOCUS_INWARD"),
            "outward": properties.Switch(name="FOCUS_OUTWARD"),
        },
    )


def FocusSpeed(  # noqa: PLR0913
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
        "FOCUS_SPEED",
        (("speed", "FOCUS_SPEED_VALUE"),),
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


def FocusTimer(  # noqa: PLR0913
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
        "FOCUS_TIMER",
        (("timer", "FOCUS_TIMER_VALUE"),),
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


def _focus_reverse(enabled_name, disabled_name, *, label, default, state, perm, timeout, enabled):  # noqa: PLR0913
    return switch_vector(
        "FOCUS_REVERSE_MOTION",
        (("enable", enabled_name), ("disable", disabled_name)),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.ONE_OF_MANY,
    )


def FocusReverseMotion(
    label=None,
    default="DISABLED",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return _focus_reverse(
        "ENABLED",
        "DISABLED",
        label=label,
        default=default,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
    )


def FocusReverseMotionIndi(
    label=None,
    default="INDI_DISABLED",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return _focus_reverse(
        "INDI_ENABLED",
        "INDI_DISABLED",
        label=label,
        default=default,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
    )


def FocusAbortMotion(
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return switch_vector(
        "FOCUS_ABORT_MOTION",
        (("abort", "ABORT"),),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.AT_MOST_ONE,
    )


def FocusSync(  # noqa: PLR0913
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
        "FOCUS_SYNC",
        (("position", "FOCUS_SYNC_VALUE"),),
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
