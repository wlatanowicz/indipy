from indi.device import properties
from indi.device.properties import const

_PARK_AXES = {
    "equatorial": (("ra", "PARK_RA"), ("dec", "PARK_DEC")),
    "horizontal": (("az", "PARK_AZ"), ("alt", "PARK_ALT")),
}

_SLEW_RATES = (
    ("guide", "SLEW_GUIDE"),
    ("centering", "SLEW_CENTERING"),
    ("find", "SLEW_FIND"),
    ("max", "SLEW_MAX"),
)


def _track_modes(custom):
    members = [("sidereal", "TRACK_SIDEREAL"), ("solar", "TRACK_SOLAR"), ("lunar", "TRACK_LUNAR")]
    if custom:
        members.append(("custom", "TRACK_CUSTOM"))
    return tuple(members)


def EquatorialCoord(  # noqa: PLR0913
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
        name="EQUATORIAL_COORD",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "ra": properties.Number(name="RA", default=default, min=min, max=max, step=step),
            "dec": properties.Number(name="DEC", default=default, min=min, max=max, step=step),
        },
    )


def EquatorialEodCoord(  # noqa: PLR0913
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
        name="EQUATORIAL_EOD_COORD",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "ra": properties.Number(name="RA", default=default, min=min, max=max, step=step),
            "dec": properties.Number(name="DEC", default=default, min=min, max=max, step=step),
        },
    )


def TargetEodCoord(  # noqa: PLR0913
    label=None,
    default=0,
    min=0,
    max=0,
    step=0,
    state=const.State.OK,
    perm=const.Permissions.READ_ONLY,
    timeout=0,
    enabled=True,
):
    return properties.NumberVector(
        name="TARGET_EOD_COORD",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "ra": properties.Number(name="RA", default=default, min=min, max=max, step=step),
            "dec": properties.Number(name="DEC", default=default, min=min, max=max, step=step),
        },
    )


def HorizontalCoord(  # noqa: PLR0913
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
        name="HORIZONTAL_COORD",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "alt": properties.Number(name="ALT", default=default, min=min, max=max, step=step),
            "az": properties.Number(name="AZ", default=default, min=min, max=max, step=step),
        },
    )


def OnCoordSet(
    label=None,
    default="SLEW",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="ON_COORD_SET",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.ONE_OF_MANY,
        elements={
            "slew": properties.Switch(name="SLEW"),
            "track": properties.Switch(name="TRACK"),
            "sync": properties.Switch(name="SYNC"),
        },
    )


def TelescopeMotionNS(
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="TELESCOPE_MOTION_NS",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.AT_MOST_ONE,
        elements={
            "north": properties.Switch(name="MOTION_NORTH"),
            "south": properties.Switch(name="MOTION_SOUTH"),
        },
    )


def TelescopeMotionWE(
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="TELESCOPE_MOTION_WE",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.AT_MOST_ONE,
        elements={
            "west": properties.Switch(name="MOTION_WEST"),
            "east": properties.Switch(name="MOTION_EAST"),
        },
    )


def TelescopeTimedGuideNS(  # noqa: PLR0913
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
        name="TELESCOPE_TIMED_GUIDE_NS",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "north": properties.Number(name="TIMED_GUIDE_N", default=default, min=min, max=max, step=step),
            "south": properties.Number(name="TIMED_GUIDE_S", default=default, min=min, max=max, step=step),
        },
    )


def TelescopeTimedGuideWE(  # noqa: PLR0913
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
        name="TELESCOPE_TIMED_GUIDE_WE",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "west": properties.Number(name="TIMED_GUIDE_W", default=default, min=min, max=max, step=step),
            "east": properties.Number(name="TIMED_GUIDE_E", default=default, min=min, max=max, step=step),
        },
    )


def TelescopeSlewRate(  # noqa: PLR0913
    label=None,
    default="SLEW_GUIDE",
    extra=(),
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    members = [*_SLEW_RATES, *((name.lower(), name) for name in extra)]
    return properties.SwitchVector(
        name="TELESCOPE_SLEW_RATE",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.ONE_OF_MANY,
        elements={key: properties.Switch(name=wire_name) for key, wire_name in members},
    )


def TelescopePark(
    label=None,
    default="UNPARK",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="TELESCOPE_PARK",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.ONE_OF_MANY,
        elements={
            "park": properties.Switch(name="PARK"),
            "unpark": properties.Switch(name="UNPARK"),
        },
    )


def TelescopeParkPosition(  # noqa: PLR0913
    label=None,
    default=0,
    min=0,
    max=0,
    step=0,
    system="equatorial",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    try:
        members = _PARK_AXES[system]
    except KeyError:
        raise ValueError("system must be 'equatorial' or 'horizontal'") from None
    return properties.NumberVector(
        name="TELESCOPE_PARK_POSITION",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            key: properties.Number(name=wire_name, default=default, min=min, max=max, step=step)
            for key, wire_name in members
        },
    )


def TelescopeParkOption(
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="TELESCOPE_PARK_OPTION",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.AT_MOST_ONE,
        elements={
            "current": properties.Switch(name="PARK_CURRENT"),
            "default": properties.Switch(name="PARK_DEFAULT"),
            "write": properties.Switch(name="PARK_WRITE_DATA"),
        },
    )


def TelescopeAbortMotion(
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="TELESCOPE_ABORT_MOTION",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.AT_MOST_ONE,
        elements={"abort": properties.Switch(name="ABORT_MOTION")},
    )


def TelescopeTrackRate(  # noqa: PLR0913
    label=None,
    default="TRACK_SIDEREAL",
    custom=False,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="TELESCOPE_TRACK_RATE",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.ONE_OF_MANY,
        elements={key: properties.Switch(name=wire_name) for key, wire_name in _track_modes(custom)},
    )


def TelescopeTrackMode(  # noqa: PLR0913
    label=None,
    default="TRACK_SIDEREAL",
    custom=False,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="TELESCOPE_TRACK_MODE",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.ONE_OF_MANY,
        elements={key: properties.Switch(name=wire_name) for key, wire_name in _track_modes(custom)},
    )


def TelescopeAxisTrackRate(  # noqa: PLR0913
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
        name="TELESCOPE_TRACK_RATE",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "ra": properties.Number(name="TRACK_RATE_RA", default=default, min=min, max=max, step=step),
            "de": properties.Number(name="TRACK_RATE_DE", default=default, min=min, max=max, step=step),
        },
    )


def TelescopeInfo(  # noqa: PLR0913
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
        name="TELESCOPE_INFO",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "aperture": properties.Number(name="TELESCOPE_APERTURE", default=default, min=min, max=max, step=step),
            "focal_length": properties.Number(
                name="TELESCOPE_FOCAL_LENGTH",
                default=default,
                min=min,
                max=max,
                step=step,
            ),
            "guider_aperture": properties.Number(name="GUIDER_APERTURE", default=default, min=min, max=max, step=step),
            "guider_focal_length": properties.Number(
                name="GUIDER_FOCAL_LENGTH",
                default=default,
                min=min,
                max=max,
                step=step,
            ),
        },
    )


def TelescopePierSide(
    label=None,
    default="PIER_EAST",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="TELESCOPE_PIER_SIDE",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.ONE_OF_MANY,
        elements={
            "east": properties.Switch(name="PIER_EAST"),
            "west": properties.Switch(name="PIER_WEST"),
        },
    )
