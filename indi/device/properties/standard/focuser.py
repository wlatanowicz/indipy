from indi.device import properties
from indi.device.properties import const


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
    return properties.NumberVector(
        name="FOCUS_SPEED",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "speed": properties.Number(name="FOCUS_SPEED_VALUE", default=default, min=min, max=max, step=step),
        },
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
    return properties.NumberVector(
        name="FOCUS_TIMER",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "timer": properties.Number(name="FOCUS_TIMER_VALUE", default=default, min=min, max=max, step=step),
        },
    )


def FocusReverseMotion(
    label=None,
    default="DISABLED",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="FOCUS_REVERSE_MOTION",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.ONE_OF_MANY,
        elements={
            "enable": properties.Switch(name="ENABLED"),
            "disable": properties.Switch(name="DISABLED"),
        },
    )


def FocusReverseMotionIndi(
    label=None,
    default="INDI_DISABLED",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="FOCUS_REVERSE_MOTION",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.ONE_OF_MANY,
        elements={
            "enable": properties.Switch(name="INDI_ENABLED"),
            "disable": properties.Switch(name="INDI_DISABLED"),
        },
    )


def FocusAbortMotion(
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="FOCUS_ABORT_MOTION",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.AT_MOST_ONE,
        elements={"abort": properties.Switch(name="ABORT")},
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
    return properties.NumberVector(
        name="FOCUS_SYNC",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "position": properties.Number(name="FOCUS_SYNC_VALUE", default=default, min=min, max=max, step=step),
        },
    )
