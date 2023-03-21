import pytest

from indi import message
from indi.message import const, def_parts, one_parts

xml_header = b'<?xml version="1.0"?>\n'

messages = [
    (
        b'<getProperties device="CAMERA" version="1.7" />',
        message.GetProperties(version="1.7", device="CAMERA"),
    ),
    (
        b'<getProperties version="1.7" />',
        message.GetProperties(version="1.7"),
    ),
    (
        b'<enableBLOB device="CAMERA">Also</enableBLOB>',
        message.EnableBLOB(device="CAMERA", value=const.BLOBEnable.ALSO),
    ),
    (
        b'<setTextVector device="CAMERA" name="EXPOSE" state="Alert">'
        b'<oneText name="EXPOSE_TIME">2.0</oneText>'
        b"</setTextVector>",
        message.SetTextVector(
            device="CAMERA",
            name="EXPOSE",
            state=const.State.ALERT,
            children=[one_parts.OneText(name="EXPOSE_TIME", value="2.0")],
        ),
    ),
    (
        b'<newTextVector device="CAMERA" name="EXPOSE">'
        b'<oneText name="EXPOSE_TIME">2.0</oneText>'
        b"</newTextVector>",
        message.NewTextVector(
            device="CAMERA",
            name="EXPOSE",
            children=[one_parts.OneText(name="EXPOSE_TIME", value="2.0")],
        ),
    ),
    (
        b'<defTextVector device="CAMERA" name="EXPOSE" perm="ro" state="Busy">'
        b'<defText name="EXPOSE_TIME">2.0</defText>'
        b"</defTextVector>",
        message.DefTextVector(
            device="CAMERA",
            name="EXPOSE",
            perm=const.Permissions.READ_ONLY,
            state=const.State.BUSY,
            children=[def_parts.DefText(name="EXPOSE_TIME", value="2.0")],
        ),
    ),
]


@pytest.mark.parametrize("in_xml, in_msg", messages)
def test_from_string(in_xml, in_msg):
    msg = message.IndiMessage.from_string(in_xml)
    # self.assertDictEqual(in_msg.__dict__, msg.__dict__)
    assert in_msg == msg


@pytest.mark.parametrize("in_xml, in_msg", messages)
def test_to_string(in_xml, in_msg):
    xml = in_msg.to_string()
    expected = xml_header + in_xml + b"\n"
    assert expected == xml
