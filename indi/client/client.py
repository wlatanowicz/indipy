from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Any, Callable, Dict, Iterable, List, Optional, Type

import indi
from indi import message
from indi.client import events
from indi.client.device import Device
from indi.message import IndiMessage, const

logger = logging.getLogger(__name__)


class _CallbackConfig:
    def __init__(
        self,
        device: Optional[str],
        vector: Optional[str],
        element: Optional[str],
        event_type: Type[events.BaseEvent],
        callback: Callable,
        uuid: uuid.UUID,
    ):
        self.device = device
        self.vector = vector
        self.element = element
        self.event_type = event_type
        self.callback = callback
        self.uuid = uuid

    def accepts_event(self, event: events.BaseEvent) -> bool:
        """Checks if event should be processed by callbacked associated with this configuration.

        :param event: An event
        :type event: events.BaseEvent
        :return: True if event should be processed
        :rtype: bool
        """
        return (
            self.device
            in (
                None,
                event.device.name if event.device else None,
            )
            and self.vector
            in (
                None,
                event.vector.name if event.vector else None,
            )
            and self.element
            in (
                None,
                event.element.name if event.element else None,
            )
            and isinstance(event, self.event_type)
        )


class _EventWaitResult:
    def __init__(self) -> None:
        self.event: Optional[events.BaseEvent] = None
        self.timeout = False


class BaseClient:
    def __init__(self) -> None:
        """Constructor for INDI client."""
        self.devices: Dict[str, Device] = {}
        self.callbacks: List[_CallbackConfig] = []

    def __getitem__(self, key) -> Device:
        return self.devices[key]

    def __contains__(self, key) -> bool:
        return key in self.devices

    def get_device(self, name: str) -> Optional[Device]:
        return self.devices.get(name)

    def list_devices(self) -> Iterable[str]:
        """Lists all known device names.

        :return: List of all known device names
        :rtype: Iterable[str]
        """
        return self.devices.keys()

    def set_device(self, name: str, device: Device):
        self.devices[name] = device
        self.blob_handshake(name)

    def process_message(self, msg: IndiMessage):
        device = None
        if isinstance(msg, message.DefVector):
            device = self.get_device(msg.device)
            if not device:
                device = Device(self, msg.device)
                self.set_device(msg.device, device)

        if isinstance(msg, message.SetVector):
            device = self.get_device(msg.device)

        if isinstance(msg, message.DelProperty):
            device = self.get_device(msg.device)

        if device:
            device.process_message(msg)

    def send_message(self, msg: IndiMessage):
        """Sends INDI message to server using control connection.

        :param msg: INDI message to be sent
        :type msg: IndiMessage
        """
        raise NotImplementedError()

    def onevent(
        self,
        *,
        callback: Callable,
        device: Optional[str] = None,
        vector: Optional[str] = None,
        element: Optional[str] = None,
        event_type: Type[events.BaseEvent] = events.BaseEvent,
    ) -> uuid.UUID:
        """Attaches event callback.

        :param callback: Callback
        :type callback: Callable
        :param device: Optional device name, defaults to None
        :type device: str, optional
        :param vector: Optional vector name, defaults to None
        :type vector: str, optional
        :param element: Optional element name, defaults to None
        :type element: str, optional
        :param event_type: Optional event type, defaults to events.BaseEvent
        :type event_type: Type[events.BaseEvent], optional
        :return: UUID of created event attachment
        :rtype: uuid
        """
        uid = uuid.uuid4()
        callback_config = _CallbackConfig(
            device=device,
            vector=vector,
            element=element,
            event_type=event_type,
            callback=callback,
            uuid=uid,
        )

        self.callbacks.append(callback_config)
        return uid

    def rmonevent(
        self,
        uuid: Optional[uuid.UUID] = None,
        device: Optional[str] = None,
        vector: Optional[str] = None,
        element: Optional[str] = None,
        event_type: Optional[Type[events.BaseEvent]] = None,
        callback: Optional[Callable] = None,
    ):
        to_rm = list()
        for cb in self.callbacks:
            if (
                uuid
                in (
                    None,
                    cb.uuid,
                )
                and device
                in (
                    None,
                    cb.device,
                )
                and vector
                in (
                    None,
                    cb.vector,
                )
                and element
                in (
                    None,
                    cb.element,
                )
                and event_type
                in (
                    None,
                    cb.event_type,
                )
                and callback in (None, cb.callback)
            ):
                to_rm.append(cb)

        for cb in to_rm:
            self.callbacks.remove(cb)

    async def waitforevent(
        self,
        device: Optional[str] = None,
        vector: Optional[str] = None,
        element: Optional[str] = None,
        event_type: Type[events.BaseEvent] = events.BaseEvent,
        expect: Any = None,
        initial: Any = None,
        check: Optional[Callable] = None,
        timeout: Optional[Optional[float]] = None,
        polling_enabled: bool = True,
        polling_delay: float = 1.0,
        polling_interval: float = 1.0,
    ):
        assert 1 == sum(
            1
            for _ in filter(
                None.__ne__,
                (
                    expect,
                    initial,
                    check,
                ),
            )
        ), "Exactly one of `expect`, `initial`, `check` has to be passed"

        lock = asyncio.Event()
        result = _EventWaitResult()

        def cb(event: events.BaseEvent):
            release = False

            if check is not None:
                if check(event):
                    release = True

            if expect is not None:
                if isinstance(event, events.ValueUpdate):
                    if event.new_value == expect:
                        release = True
                if isinstance(event, events.StateUpdate):
                    if event.new_state == expect:
                        release = True

            if initial is not None:
                if isinstance(event, events.ValueUpdate):
                    if event.new_value != initial:
                        release = True
                if isinstance(event, events.StateUpdate):
                    if event.new_state != initial:
                        release = True

            if release:
                result.event = event
                lock.set()

        if polling_enabled:

            async def poll():
                kwargs = {}
                if device:
                    kwargs["device"] = device
                if vector:
                    kwargs["name"] = vector

                msg = message.GetProperties(version=indi.__protocol_version__, **kwargs)

                await asyncio.sleep(polling_delay)
                while not lock.is_set():
                    self.send_message(msg)
                    await asyncio.sleep(polling_interval)

            asyncio.get_running_loop().create_task(poll())

        async def timeout_check():
            await asyncio.sleep(timeout)
            if not lock.is_set():
                result.timeout = True
                lock.set()

        uid = self.onevent(
            device=device,
            vector=vector,
            element=element,
            event_type=event_type,
            callback=cb,
        )

        if timeout is not None and timeout > 0:
            asyncio.get_running_loop().create_task(timeout_check())

        await lock.wait()

        self.rmonevent(uuid=uid)

        if result.timeout:
            raise Exception("Timeout occurred")

        return result.event

    def trigger_event(self, event: events.BaseEvent):
        for callback in self.callbacks:
            if callback.accepts_event(event):
                try:
                    callback.callback(event)
                except:
                    logger.exception("Error in event handler")

    def handshake(self, device=None, name=None, version=indi.__protocol_version__):
        self.send_message(
            message.GetProperties(version=version, device=device, name=name)
        )

    def blob_handshake(self, device):
        self.send_message(
            message.EnableBLOB(device=device, value=const.BLOBEnable.NEVER)
        )


class Client(BaseClient):
    def __init__(self, control_connection, blob_connection):
        super().__init__()
        self.control_connection = control_connection
        self.blob_connection = blob_connection
        self.control_connection_handler = None
        self.blob_connection_handler = None

    def send_message(self, msg: IndiMessage):
        """Sends INDI message to server using control connection.

        :param msg: INDI message to be sent
        :type msg: IndiMessage
        """
        self.control_connection_handler.send_message(msg)

    def blob_handshake(self, device):
        super().blob_handshake(device)
        self.blob_connection_handler.send_message(
            message.EnableBLOB(device=device, value=const.BLOBEnable.ONLY)
        )

    async def start(self):
        """Starts client and connects to the server.

        Connects both connections (control and blob) and sends initial GetProperties message to the server.
        """
        self.control_connection_handler = await self.control_connection.connect(
            self.process_message
        )
        self.blob_connection_handler = await self.blob_connection.connect(
            self.process_message
        )

        asyncio.get_running_loop().create_task(
            self.control_connection_handler.wait_for_messages()
        )
        asyncio.get_running_loop().create_task(
            self.blob_connection_handler.wait_for_messages()
        )

        self.handshake()

    def stop(self):
        self.control_connection_handler.close()
        self.blob_connection_handler.close()
