from indi.device.properties import const
from indi.device.properties.standard._vector import number_vector, text_vector


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
    return number_vector(
        "FILTER_SLOT",
        (("slot", "FILTER_SLOT_VALUE"),),
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


def FilterName(
    label=None,
    default="",
    state=const.State.OK,
    perm=const.Permissions.READ_WRITE,
    timeout=0,
    enabled=True,
):
    return text_vector(
        "FILTER_NAME",
        (("filter_name", "FILTER_NAME_VALUE"),),
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default=default,
    )
