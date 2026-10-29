from indi.device.properties import const
from indi.device.properties.standard._vector import number_vector, switch_vector

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
    return number_vector(
        "EQUATORIAL_COORD",
        (("ra", "RA"), ("dec", "DEC")),
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
    return number_vector(
        "EQUATORIAL_EOD_COORD",
        (("ra", "RA"), ("dec", "DEC")),
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
    return number_vector(
        "TARGET_EOD_COORD",
        (("ra", "RA"), ("dec", "DEC")),
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
    return number_vector(
        "HORIZONTAL_COORD",
        (("alt", "ALT"), ("az", "AZ")),
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


def OnCoordSet(
    label=None,
    default="SLEW",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return switch_vector(
        "ON_COORD_SET",
        (("slew", "SLEW"), ("track", "TRACK"), ("sync", "SYNC")),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.ONE_OF_MANY,
    )


def TelescopeMotionNS(
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return switch_vector(
        "TELESCOPE_MOTION_NS",
        (("north", "MOTION_NORTH"), ("south", "MOTION_SOUTH")),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.AT_MOST_ONE,
    )


def TelescopeMotionWE(
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return switch_vector(
        "TELESCOPE_MOTION_WE",
        (("west", "MOTION_WEST"), ("east", "MOTION_EAST")),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.AT_MOST_ONE,
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
    return number_vector(
        "TELESCOPE_TIMED_GUIDE_NS",
        (("north", "TIMED_GUIDE_N"), ("south", "TIMED_GUIDE_S")),
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
    return number_vector(
        "TELESCOPE_TIMED_GUIDE_WE",
        (("west", "TIMED_GUIDE_W"), ("east", "TIMED_GUIDE_E")),
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
    return switch_vector(
        "TELESCOPE_SLEW_RATE",
        members,
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.ONE_OF_MANY,
    )


def TelescopePark(
    label=None,
    default="UNPARK",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return switch_vector(
        "TELESCOPE_PARK",
        (("park", "PARK"), ("unpark", "UNPARK")),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.ONE_OF_MANY,
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
    return number_vector(
        "TELESCOPE_PARK_POSITION",
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


def TelescopeParkOption(
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return switch_vector(
        "TELESCOPE_PARK_OPTION",
        (("current", "PARK_CURRENT"), ("default", "PARK_DEFAULT"), ("write", "PARK_WRITE_DATA")),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.AT_MOST_ONE,
    )


def TelescopeAbortMotion(
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return switch_vector(
        "TELESCOPE_ABORT_MOTION",
        (("abort", "ABORT_MOTION"),),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.AT_MOST_ONE,
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
    return switch_vector(
        "TELESCOPE_TRACK_RATE",
        _track_modes(custom),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.ONE_OF_MANY,
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
    return switch_vector(
        "TELESCOPE_TRACK_MODE",
        _track_modes(custom),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.ONE_OF_MANY,
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
    return number_vector(
        "TELESCOPE_TRACK_RATE",
        (("ra", "TRACK_RATE_RA"), ("de", "TRACK_RATE_DE")),
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
    return number_vector(
        "TELESCOPE_INFO",
        (
            ("aperture", "TELESCOPE_APERTURE"),
            ("focal_length", "TELESCOPE_FOCAL_LENGTH"),
            ("guider_aperture", "GUIDER_APERTURE"),
            ("guider_focal_length", "GUIDER_FOCAL_LENGTH"),
        ),
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


def TelescopePierSide(
    label=None,
    default="PIER_EAST",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return switch_vector(
        "TELESCOPE_PIER_SIDE",
        (("east", "PIER_EAST"), ("west", "PIER_WEST")),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.ONE_OF_MANY,
    )
