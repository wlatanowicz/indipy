from indi.device import properties
from indi.device.properties import const


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
    return properties.SwitchVector(
        name="GUIDER_ABORT_EXPOSURE" if guider else "CCD_ABORT_EXPOSURE",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.AT_MOST_ONE,
        elements={"abort": properties.Switch(name="ABORT")},
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
    return properties.NumberVector(
        name="GUIDER_FRAME" if guider else "CCD_FRAME",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "x": properties.Number(name="X", default=default, min=min, max=max, step=step),
            "y": properties.Number(name="Y", default=default, min=min, max=max, step=step),
            "width": properties.Number(name="WIDTH", default=default, min=min, max=max, step=step),
            "height": properties.Number(name="HEIGHT", default=default, min=min, max=max, step=step),
        },
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
    return properties.NumberVector(
        name="GUIDER_TEMPERATURE" if guider else "CCD_TEMPERATURE",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "temperature": properties.Number(
                name="GUIDER_TEMPERATURE_VALUE" if guider else "CCD_TEMPERATURE_VALUE",
                default=default,
                min=min,
                max=max,
                step=step,
            )
        },
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
    return properties.SwitchVector(
        name="GUIDER_COOLER" if guider else "CCD_COOLER",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.ONE_OF_MANY,
        elements={
            "on": properties.Switch(name="COOLER_ON"),
            "off": properties.Switch(name="COOLER_OFF"),
        },
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
    return properties.NumberVector(
        name="GUIDER_COOLER_POWER" if guider else "CCD_COOLER_POWER",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "power": properties.Number(
                name="GUIDER_COOLER_VALUE" if guider else "CCD_COOLER_VALUE",
                default=default,
                min=min,
                max=max,
                step=step,
            )
        },
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
    return properties.SwitchVector(
        name="GUIDER_FRAME_TYPE" if guider else "CCD_FRAME_TYPE",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.ONE_OF_MANY,
        elements={
            "light": properties.Switch(name="FRAME_LIGHT"),
            "bias": properties.Switch(name="FRAME_BIAS"),
            "dark": properties.Switch(name="FRAME_DARK"),
            "flat": properties.Switch(name="FRAME_FLAT"),
        },
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
    return properties.NumberVector(
        name="GUIDER_BINNING" if guider else "CCD_BINNING",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "horizontal": properties.Number(name="HOR_BIN", default=default, min=min, max=max, step=step),
            "vertical": properties.Number(name="VER_BIN", default=default, min=min, max=max, step=step),
        },
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
    return properties.SwitchVector(
        name="GUIDER_COMPRESSION" if guider else "CCD_COMPRESSION",
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


def FrameReset(  # noqa: PLR0913
    label=None,
    default=None,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
    guider=False,
):
    return properties.SwitchVector(
        name="GUIDER_FRAME_RESET" if guider else "CCD_FRAME_RESET",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.AT_MOST_ONE,
        elements={"reset": properties.Switch(name="RESET")},
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
    return properties.NumberVector(
        name="GUIDER_INFO" if guider else "CCD_INFO",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "max_x": properties.Number(name="CCD_MAX_X", default=default, min=min, max=max, step=step),
            "max_y": properties.Number(name="CCD_MAX_Y", default=default, min=min, max=max, step=step),
            "pixel_size": properties.Number(name="CCD_PIXEL_SIZE", default=default, min=min, max=max, step=step),
            "pixel_size_x": properties.Number(name="CCD_PIXEL_SIZE_X", default=default, min=min, max=max, step=step),
            "pixel_size_y": properties.Number(name="CCD_PIXEL_SIZE_Y", default=default, min=min, max=max, step=step),
            "bits_per_pixel": properties.Number(name="CCD_BITSPERPIXEL", default=default, min=min, max=max, step=step),
        },
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
    return properties.TextVector(
        name="GUIDER_CFA" if guider else "CCD_CFA",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "offset_x": properties.Text(name="CFA_OFFSET_X", default=default),
            "offset_y": properties.Text(name="CFA_OFFSET_Y", default=default),
            "type": properties.Text(name="CFA_TYPE", default=default),
        },
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
    return properties.BLOBVector(
        name=wire_name,
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={"image": properties.BLOB(name=wire_name)},
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
    return properties.SwitchVector(
        name="CCD_VIDEO_STREAM",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.ONE_OF_MANY,
        elements={
            "on": properties.Switch(name="STREAM_ON"),
            "off": properties.Switch(name="STREAM_OFF"),
        },
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
    return properties.NumberVector(
        name="STREAMING_EXPOSURE",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "exposure": properties.Number(
                name="STREAMING_EXPOSURE_VALUE",
                default=default,
                min=min,
                max=max,
                step=step,
            ),
            "divisor": properties.Number(
                name="STREAMING_DIVISOR_VALUE",
                default=default,
                min=min,
                max=max,
                step=step,
            ),
        },
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
    return properties.NumberVector(
        name="FPS",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "estimated": properties.Number(name="EST_FPS", default=default, min=min, max=max, step=step),
            "average": properties.Number(name="AVG_FPS", default=default, min=min, max=max, step=step),
        },
    )


def RecordFile(
    label=None,
    default="",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.TextVector(
        name="RECORD_FILE",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "directory": properties.Text(name="RECORD_FILE_DIR", default=default),
            "file_name": properties.Text(name="RECORD_FILE_NAME", default=default),
        },
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
    return properties.NumberVector(
        name="RECORD_OPTIONS",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "duration": properties.Number(name="RECORD_DURATION", default=default, min=min, max=max, step=step),
            "frames": properties.Number(name="RECORD_FRAME_TOTAL", default=default, min=min, max=max, step=step),
        },
    )


def RecordStream(
    label=None,
    default="RECORD_OFF",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.SwitchVector(
        name="RECORD_STREAM",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=const.SwitchRule.ONE_OF_MANY,
        elements={
            "on": properties.Switch(name="RECORD_ON"),
            "duration": properties.Switch(name="RECORD_DURATION_ON"),
            "frames": properties.Switch(name="RECORD_FRAME_ON"),
            "off": properties.Switch(name="RECORD_OFF"),
        },
    )
