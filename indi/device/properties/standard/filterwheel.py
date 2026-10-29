from indi.device import properties
from indi.device.properties import const


def FilterSlot(  # noqa: PLR0913
    label=None,
    default=1,
    min=1,
    max=1,
    step=1,
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.NumberVector(
        name="FILTER_SLOT",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            "slot": properties.Number(name="FILTER_SLOT_VALUE", default=default, min=min, max=max, step=step),
        },
    )


def FilterName(
    label=None,
    default="",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return properties.TextVector(
        name="FILTER_NAME",
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={"filter_name": properties.Text(name="FILTER_NAME_VALUE", default=default)},
    )
