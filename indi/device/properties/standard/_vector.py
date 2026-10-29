from indi.device import properties


def number_vector(name, elements, *, label, state, perm, timeout, enabled, default, min, max, step):  # noqa: PLR0913
    return properties.NumberVector(
        name=name,
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={
            key: properties.Number(name=wire_name, default=default, min=min, max=max, step=step)
            for key, wire_name in elements
        },
    )


def text_vector(name, elements, *, label, state, perm, timeout, enabled, default):  # noqa: PLR0913
    return properties.TextVector(
        name=name,
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={key: properties.Text(name=wire_name, default=default) for key, wire_name in elements},
    )


def switch_vector(name, elements, *, label, state, perm, timeout, enabled, default, rule):  # noqa: PLR0913
    return properties.SwitchVector(
        name=name,
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        default_on=default,
        rule=rule,
        elements={key: properties.Switch(name=wire_name) for key, wire_name in elements},
    )


def blob_vector(name, element, *, label, state, perm, timeout, enabled):  # noqa: PLR0913
    key, wire_name = element
    return properties.BLOBVector(
        name=name,
        label=label,
        state=state,
        perm=perm,
        timeout=timeout,
        enabled=enabled,
        elements={key: properties.BLOB(name=wire_name)},
    )


def chip_name(name, guider):
    if guider and name.startswith("CCD_"):
        return "GUIDER_" + name.removeprefix("CCD_")
    return name


def chip_members(members, guider, *, keep=False):
    if keep or not guider:
        return tuple(members)
    return tuple((key, chip_name(wire_name, True)) for key, wire_name in members)
