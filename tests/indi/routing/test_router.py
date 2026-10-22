from unittest import mock

import pytest

from indi import message
from indi.message import const
from indi.routing import Router

messages = [
    ("SOME_DEVICE", ((True, True), (False, False))),
    (None, ((True, True), (False, False))),
]


@pytest.mark.parametrize(("message_device", "device_specs"), messages)
def test_message_from_client(message_device, device_specs):
    devices = [
        {
            "mock": mock.Mock(),
            "accepts": accepts,
            "processes": processes,
        }
        for accepts, processes in device_specs
    ]

    msg = message.GetProperties(version="2.0", device=message_device)
    router = Router()

    for device in devices:
        device["mock"].accepts.return_value = device["accepts"]
        router.register_device(device["mock"])

    router.process_message(message=msg)

    for device in devices:
        device["mock"].accepts.assert_called_once_with(msg.device)

        if device["processes"]:
            device["mock"].message_from_client.assert_called_once_with(msg)


def test_message_from_device():
    router = Router()

    client = mock.Mock()

    router.register_client(client)

    msg = message.DelProperty(device="SOME_DEVICE")

    router.process_message(msg)

    client.message_from_device.assert_called_once_with(msg)


def _device_message(kind: str) -> message.IndiMessage:
    if kind == "blob-value":
        return message.SetBLOBVector(device="SOME_DEVICE", name="VECTOR", state=const.State.OK)
    if kind == "blob-definition":
        return message.DefBLOBVector(
            device="SOME_DEVICE",
            name="VECTOR",
            state=const.State.OK,
            perm=const.Permissions.READ_ONLY,
        )
    return message.SetNumberVector(device="SOME_DEVICE", name="VECTOR", state=const.State.OK)


@pytest.mark.parametrize(
    ("policy", "kind", "forwarded"),
    [
        (None, "number", True),
        (None, "blob-value", False),
        (None, "blob-definition", True),
        (const.BLOBEnable.NEVER, "number", True),
        (const.BLOBEnable.NEVER, "blob-value", False),
        (const.BLOBEnable.NEVER, "blob-definition", True),
        (const.BLOBEnable.ALSO, "number", True),
        (const.BLOBEnable.ALSO, "blob-value", True),
        (const.BLOBEnable.ALSO, "blob-definition", True),
        (const.BLOBEnable.ONLY, "number", False),
        (const.BLOBEnable.ONLY, "blob-value", True),
        (const.BLOBEnable.ONLY, "blob-definition", True),
    ],
)
def test_blob_policy_filters_device_messages(policy, kind, forwarded):
    router = Router()
    client = mock.Mock()
    router.register_client(client)

    if policy is not None:
        router.process_message(
            message.EnableBLOB(device="SOME_DEVICE", value=policy),
            sender=client,
        )

    msg = _device_message(kind)
    router.process_message(msg)

    if forwarded:
        client.message_from_device.assert_called_once_with(msg)
    else:
        client.message_from_device.assert_not_called()
