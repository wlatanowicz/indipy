import pytest

from unittest import mock
from unittest.mock import patch

from indi import message
from indi.routing import Device, Router


messages = [
    ("SOME_DEVICE", ((True, True), (False, False))),
    (None, ((None, True), (None, True))),
]


@pytest.mark.parametrize('message_device, device_specs', messages)
def test_message_from_client(message_device, device_specs):
    devices = [
        {"mock": mock.Mock(), "accepts": accepts, "processes": processes,}
        for accepts,processes  in device_specs
    ]

    msg = message.GetProperties(version="2.0", device=message_device)
    router = Router()

    for device in devices:
        device["mock"].accepts.return_value = device["accepts"]
        router.register_device(device["mock"])

    router.process_message(message=msg)

    for device in devices:
        if message_device is not None:
            device["mock"].accepts.assert_called_once_with(msg.device)
        else:
            device["mock"].accepts.assert_not_called()

        if device["processes"]:
            device["mock"].message_from_client.assert_called_once_with(msg)


def test_message_from_device():
    router = Router()

    client = mock.Mock()

    router.register_client(client)

    msg = message.DelProperty(device="SOME_DEVICE")

    router.process_message(msg)

    client.message_from_device.assert_called_once_with(msg)
