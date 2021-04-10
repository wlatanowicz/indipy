from indi.device import properties
from indi.device.properties import const


def AbsolutePosition(
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
        elements=dict(
            position=properties.Number(
                name="FOCUS_ABSOLUTE_POSITION",
                default=default,
                min=min,
                max=max,
                step=step,
            )
        ),
    )


def RelativePosition(
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
        elements=dict(
            position=properties.Number(
                name="FOCUS_RELATIVE_POSITION", min=min, max=max, step=step
            )
        ),
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
        elements=dict(max=properties.Number(name="FOCUS_MAX_VALUE", default=default)),
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
        elements=dict(
            inward=properties.Switch(name="FOCUS_INWARD"),
            outward=properties.Switch(name="FOCUS_OUTWARD"),
        ),
    )
