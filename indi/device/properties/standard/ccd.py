from indi.device import properties
from indi.device.properties import const
from indi.device.properties.standard._vector import (
    blob_vector,
    chip_members,
    chip_name,
    number_vector,
    switch_vector,
    text_vector,
)


def Exposure(  # noqa: PLR0913
    label=None,
    default=0,
    min=0,
    max=2000,
    step=0.00000001,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.NumberVector(
        name="CCD_EXPOSURE",
        elements={"time": properties.Number(name="CCD_EXPOSURE_VALUE", default=default, min=min, max=max, step=step)},
    )


def UploadMode(
    label=None,
    default="UPLOAD_CLIENT",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="UPLOAD_MODE",
        default_on=default,
        rule=const.SwitchRule.ONE_OF_MANY,
        elements={
            "client": properties.Switch(name="UPLOAD_CLIENT"),
            "local": properties.Switch(name="UPLOAD_LOCAL"),
            "both": properties.Switch(name="UPLOAD_BOTH"),
        },
    )


def AbortExposure(  # noqa: PLR0913
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
    guider=False,
):
    return switch_vector(
        chip_name("CCD_ABORT_EXPOSURE", guider),
        chip_members((("abort", "ABORT"),), guider),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.AT_MOST_ONE,
    )


def Frame(  # noqa: PLR0913
    label=None,
    default=0,
    min=0,
    max=0,
    step=0,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
    guider=False,
):
    return number_vector(
        chip_name("CCD_FRAME", guider),
        chip_members((("x", "X"), ("y", "Y"), ("width", "WIDTH"), ("height", "HEIGHT")), guider),
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


def Temperature(  # noqa: PLR0913
    label=None,
    default=0,
    min=0,
    max=0,
    step=0,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
    guider=False,
):
    return number_vector(
        chip_name("CCD_TEMPERATURE", guider),
        chip_members((("temperature", "CCD_TEMPERATURE_VALUE"),), guider),
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


def Cooler(  # noqa: PLR0913
    label=None,
    default="COOLER_OFF",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
    guider=False,
):
    return switch_vector(
        chip_name("CCD_COOLER", guider),
        chip_members((("on", "COOLER_ON"), ("off", "COOLER_OFF")), guider),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.ONE_OF_MANY,
    )


def CoolerPower(  # noqa: PLR0913
    label=None,
    default=0,
    min=0,
    max=0,
    step=0,
    state=const.State.OK,
    perm=const.Permissions.READ_ONLY,
    timeout=0,
    enabled=True,
    guider=False,
):
    return number_vector(
        chip_name("CCD_COOLER_POWER", guider),
        chip_members((("power", "CCD_COOLER_VALUE"),), guider),
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


def FrameType(  # noqa: PLR0913
    label=None,
    default="FRAME_LIGHT",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
    guider=False,
):
    return switch_vector(
        chip_name("CCD_FRAME_TYPE", guider),
        chip_members(
            (("light", "FRAME_LIGHT"), ("bias", "FRAME_BIAS"), ("dark", "FRAME_DARK"), ("flat", "FRAME_FLAT")),
            guider,
        ),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.ONE_OF_MANY,
    )


def Binning(  # noqa: PLR0913
    label=None,
    default=0,
    min=0,
    max=0,
    step=0,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
    guider=False,
):
    return number_vector(
        chip_name("CCD_BINNING", guider),
        chip_members((("horizontal", "HOR_BIN"), ("vertical", "VER_BIN")), guider),
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


def Compression(  # noqa: PLR0913
    label=None,
    default="INDI_DISABLED",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
    guider=False,
):
    return switch_vector(
        chip_name("CCD_COMPRESSION", guider),
        chip_members((("enable", "INDI_ENABLED"), ("disable", "INDI_DISABLED")), guider),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.ONE_OF_MANY,
    )


def FrameReset(  # noqa: PLR0913
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
    guider=False,
):
    return switch_vector(
        chip_name("CCD_FRAME_RESET", guider),
        chip_members((("reset", "RESET"),), guider),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.AT_MOST_ONE,
    )


def Info(  # noqa: PLR0913
    label=None,
    default=0,
    min=0,
    max=0,
    step=0,
    state=const.State.OK,
    perm=const.Permissions.READ_ONLY,
    timeout=0,
    enabled=True,
    guider=False,
):
    members = (
        ("max_x", "CCD_MAX_X"),
        ("max_y", "CCD_MAX_Y"),
        ("pixel_size", "CCD_PIXEL_SIZE"),
        ("pixel_size_x", "CCD_PIXEL_SIZE_X"),
        ("pixel_size_y", "CCD_PIXEL_SIZE_Y"),
        ("bits_per_pixel", "CCD_BITSPERPIXEL"),
    )
    return number_vector(
        chip_name("CCD_INFO", guider),
        chip_members(members, guider, keep=True),
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


def Cfa(  # noqa: PLR0913
    label=None,
    default="",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
    guider=False,
):
    return text_vector(
        chip_name("CCD_CFA", guider),
        chip_members((("offset_x", "CFA_OFFSET_X"), ("offset_y", "CFA_OFFSET_Y"), ("type", "CFA_TYPE")), guider),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
    )


def Image(
    label=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
    guider=False,
):
    wire_name = "CCD2" if guider else "CCD1"
    return blob_vector(
        wire_name,
        ("image", wire_name),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
    )


def GuiderExposure(  # noqa: PLR0913
    label=None,
    default=0,
    min=0,
    max=2000,
    step=0.00000001,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.NumberVector(
        name="GUIDER_EXPOSURE",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "time": properties.Number(
                name="GUIDER_EXPOSURE_VALUE",
                default=default,
                min=min,
                max=max,
                step=step,
            )
        },
    )


def VideoStream(
    label=None,
    default="STREAM_OFF",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return switch_vector(
        "CCD_VIDEO_STREAM",
        (("on", "STREAM_ON"), ("off", "STREAM_OFF")),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.ONE_OF_MANY,
    )


def StreamingExposure(  # noqa: PLR0913
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
        "STREAMING_EXPOSURE",
        (("exposure", "STREAMING_EXPOSURE_VALUE"), ("divisor", "STREAMING_DIVISOR_VALUE")),
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


def Fps(  # noqa: PLR0913
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
        "FPS",
        (("estimated", "EST_FPS"), ("average", "AVG_FPS")),
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


def RecordFile(
    label=None,
    default="",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return text_vector(
        "RECORD_FILE",
        (("directory", "RECORD_FILE_DIR"), ("file_name", "RECORD_FILE_NAME")),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
    )


def RecordOptions(  # noqa: PLR0913
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
        "RECORD_OPTIONS",
        (("duration", "RECORD_DURATION"), ("frames", "RECORD_FRAME_TOTAL")),
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


def RecordStream(
    label=None,
    default="RECORD_OFF",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return switch_vector(
        "RECORD_STREAM",
        (
            ("on", "RECORD_ON"),
            ("duration", "RECORD_DURATION_ON"),
            ("frames", "RECORD_FRAME_ON"),
            ("off", "RECORD_OFF"),
        ),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
        rule=const.SwitchRule.ONE_OF_MANY,
    )
