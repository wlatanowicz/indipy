import xml.etree.ElementTree as ET

from indi import message
from indi.device import Driver, properties
from indi.device.properties import standard
from indi.message import const, def_parts


class SpeedDevice(Driver):
    name = "DEVICE"

    main = properties.Group(
        "MAIN",
        vectors={
            "speed": properties.NumberVector(
                "SPEED",
                elements={"speed": properties.Number("SPEED_VALUE", default=100)},
            ),
        },
    )


class FocusMaxDevice(Driver):
    name = "FOCUSER"

    main = properties.Group(
        "MAIN",
        vectors={
            "fmax": standard.focuser.FocusMax(perm=const.Permissions.READ_ONLY),
        },
    )


def _number_element(parent: ET.Element) -> ET.Element:
    element = parent.find("defNumber")
    assert element is not None
    return element


def _assert_bounds(element: ET.Element) -> None:
    number_format = element.get("format")
    minimum = element.get("min")
    maximum = element.get("max")
    step = element.get("step")
    assert number_format is not None
    assert minimum is not None
    assert maximum is not None
    assert step is not None
    assert float(minimum) == float(maximum)


def test_number_without_bounds_serializes_min_and_max():
    element = _number_element(SpeedDevice().main.speed.to_def_message().to_xml())
    _assert_bounds(element)
    assert element.get("format") == "%f"
    assert float(element.get("min")) == 0.0
    assert float(element.get("max")) == 0.0


def test_def_number_none_bounds_are_serialized():
    vector = message.DefNumberVector(
        device="DEVICE",
        name="SPEED",
        state=const.State.OK,
        perm=const.Permissions.READ_WRITE,
        children=(def_parts.DefNumber(name="SPEED_VALUE", format=None, min=None, max=None, step=None, value="0"),),
    )
    element = _number_element(vector.to_xml())
    _assert_bounds(element)
    assert element.get("format") == "%f"
    assert element.get("step") == "0"


def test_focus_max_read_only_serializes_perm_and_bounds():
    xml = FocusMaxDevice().main.fmax.to_def_message().to_xml()
    assert xml.get("perm") == "ro"
    element = _number_element(xml)
    _assert_bounds(element)
