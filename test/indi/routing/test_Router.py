import unittest
from unittest import mock
from unittest.mock import patch

from ddt import data, ddt, unpack
from indi import message
from indi.routing import Device, Router


@ddt
class TestRouter(unittest.TestCase):
    messages = [
        ("SOME_DEVICE", ((True, True), (False, False))),
        (None, ((None, True), (None, True))),
    ]

    @data(*messages)
    @unpack
    def test_message_from_client(self, message_device, device_specs):
        devices = [
            {"mock": mock.Mock(), "accepts": ds[0], "processes": ds[1],}
            for ds in device_specs
        ]

        msg = message.GetProperties(version="2.0", device=message_device)
        router = Router()

        for device in devices:
            device["mock"].accepts.return_value = device["accepts"]
            router.register_device(device["mock"])

        router.process_message(message=msg)

        for device in devices:
            if device["accepts"] is not None:
                device["mock"].accepts.assert_called_once_with(msg.device)
            if device["processes"]:
                device["mock"].message_from_client.assert_called_once_with(msg)

    class fake_threading:
        class Thread:
            def __init__(self, target, *args, **kwargs):
                self.target = target

            def start(self):
                self.target()

    @patch("indi.routing.router.threading", new_callable=fake_threading)
    def test_message_from_device(self, mocked_threading):
        router = Router()

        client = mock.Mock()

        router.register_client(client)

        msg = message.DelProperty(device="SOME_DEVICE")

        router.process_message(msg)

        client.message_from_device.assert_called_once_with(msg)
