from indi.device import properties
from indi.device.properties import const


def Exposure(
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
        elements=dict(
            time=properties.Number(
                name="CCD_EXPOSURE_VALUE", default=default, min=min, max=max, step=step
            )
        ),
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
        elements=dict(
            client=properties.Switch(name="UPLOAD_CLIENT"),
            local=properties.Switch(name="UPLOAD_LOCAL"),
            both=properties.Switch(name="UPLOAD_BOTH"),
        ),
    )
