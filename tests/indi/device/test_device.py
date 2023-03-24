from unittest.mock import MagicMock

from indi import message
from indi.device import Driver, properties, values
from indi.message import const, one_parts


class DummyDevice(Driver):
    name = "DEVICE"

    main = properties.Group(
        "MAIN",
        vectors=dict(
            switch=properties.SwitchVector(
                "SWITCH",
                rule=properties.SwitchVector.RULES.ONE_OF_MANY,
                default_on="FIRST",
                elements=dict(
                    first=properties.Switch("FIRST"),
                    second=properties.Switch("SECOND"),
                    third=properties.Switch("THIRD"),
                ),
            ),
            number=properties.NumberVector(
                "NUMBER",
                elements=dict(
                    num=properties.Number("NUM", default=100),
                    snum=properties.Number("SNUM", default=100, format="%.3m"),
                ),
            ),
            text=properties.TextVector(
                "TEXT",
                elements=dict(
                    txt=properties.Text("TXT", default="lorem"),
                ),
            ),
            blob=properties.BLOBVector(
                "BLOB",
                elements=dict(
                    blb=properties.BLOB("BLB"),
                ),
            ),
        ),
    )


def test_device_process_new_switch_vector_message():
    msg = message.NewSwitchVector(
        device="DEVICE",
        name="SWITCH",
        children=(one_parts.OneSwitch(name="THIRD", value=const.SwitchState.ON),),
    )

    dev = DummyDevice()

    assert dev.main.switch.first.bool_value
    assert not dev.main.switch.second.bool_value
    assert not dev.main.switch.third.bool_value

    dev.message_from_client(msg)

    assert not dev.main.switch.first.bool_value
    assert not dev.main.switch.second.bool_value
    assert dev.main.switch.third.bool_value


def test_device_process_new_number_vector_message():
    msg = message.NewNumberVector(
        device="DEVICE",
        name="NUMBER",
        children=(one_parts.OneNumber(name="NUM", value=200),),
    )

    dev = DummyDevice()

    assert dev.main.number.num.value == 100

    dev.message_from_client(msg)

    assert dev.main.number.num.value == 200


def test_device_process_new_number_vector_message_sexagesimal():
    msg = message.NewNumberVector(
        device="DEVICE",
        name="NUMBER",
        children=(one_parts.OneNumber(name="SNUM", value="200:30"),),
    )

    dev = DummyDevice()

    assert dev.main.number.snum.value == 100

    dev.message_from_client(msg)

    assert dev.main.number.snum.value == 200.5


def test_device_process_new_text_vector_message():
    msg = message.NewTextVector(
        device="DEVICE",
        name="TEXT",
        children=(one_parts.OneText(name="TXT", value="ipsum"),),
    )

    dev = DummyDevice()

    assert dev.main.text.txt.value == "lorem"

    dev.message_from_client(msg)

    assert dev.main.text.txt.value == "ipsum"


def test_device_process_new_blob_vector_message():
    msg = message.NewBLOBVector(
        device="DEVICE",
        name="BLOB",
        children=(
            one_parts.OneBLOB(
                name="BLB", value="TG9yZW0gaXBzdW0=", format=".txt", size=11
            ),
        ),
    )

    dev = DummyDevice()

    assert dev.main.blob.blb.value is None

    dev.message_from_client(msg)

    assert dev.main.blob.blb.value.binary == b"Lorem ipsum"
    assert dev.main.blob.blb.value.format == ".txt"


def test_device_sends_set_text_vector_message():
    router_mock = MagicMock()
    dev = DummyDevice(router=router_mock)

    dev.main.text.txt.value = "new value"

    expected_msg = message.SetTextVector(
        device="DEVICE",
        name="TEXT",
        state=const.State.OK,
        children=(one_parts.OneText(name="TXT", value="new value"),),
    )

    router_mock.process_message.assert_called_once()
    call_msg, call_dev = router_mock.process_message.call_args[0]

    assert call_dev is dev
    assert call_msg.device == expected_msg.device
    assert call_msg.name == expected_msg.name
    assert call_msg.children == expected_msg.children


def test_device_sends_set_blob_vector_message():
    router_mock = MagicMock()
    dev = DummyDevice(router=router_mock)

    dev.main.blob.blb.value = values.BLOB(binary=b"Lorem ipsum", format=".txt")

    expected_msg = message.SetBLOBVector(
        device="DEVICE",
        name="BLOB",
        state=const.State.OK,
        children=(
            one_parts.OneBLOB(
                name="BLB", value="TG9yZW0gaXBzdW0=", size=11, format=".txt"
            ),
        ),
    )

    router_mock.process_message.assert_called_once()
    call_msg, call_dev = router_mock.process_message.call_args[0]

    assert call_dev is dev
    assert call_msg.device == expected_msg.device
    assert call_msg.name == expected_msg.name
    assert call_msg.children == expected_msg.children
