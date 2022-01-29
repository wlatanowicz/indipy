from __future__ import annotations

import logging
import threading
import time
import uuid
from typing import Any, Callable, List, Optional, Type

import indi
from indi import message
from indi.client import events
from indi.client.device import Device
from indi.client.elements import Element
from indi.client.vectors import Vector
from indi.message import IndiMessage, const

logger = logging.getLogger(__name__)


class Client:
    class CallbackConfig:
        def __init__(
            self,
            device: Optional[str],
            vector: Optional[str],
            element: Optional[str],
            event_type: Type[events.Event],
            callback: Callable,
            uuid: uuid.UUID,
        ):
            self.device = device
            self.vector = vector
            self.element = element
            self.event_type = event_type
            self.callback = callback
            self.uuid = uuid

        def accepts_event(self, event: events.Event) -> bool:
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

    def __init__(self, control_connection, blob_connection):
        self.devices = {}
        self.control_connection = control_connection
        self.blob_connection = blob_connection
        self.control_connection_handler = None
        self.blob_connection_handler = None
        self.callbacks: List[self.CallbackConfig] = []

    def __getitem__(self, key) -> Device:
        return self.devices[key]

    def __contains__(self, key) -> bool:
        return key in self.devices

    def get_device(self, name: str) -> Device:
        return self.devices.get(name)

    def list_devices(self) -> List[str]:
        return tuple(self.devices.keys())

    def set_device(self, name: str, device: Device):
        self.devices[name] = device
        self.control_connection_handler.send_message(
            message.EnableBLOB(device=name, value=const.BLOBEnable.NEVER)
        )
        self.blob_connection_handler.send_message(
            message.EnableBLOB(device=name, value=const.BLOBEnable.ONLY)
        )

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
        self.control_connection_handler.send_message(msg)

    def start(self):
        self.control_connection_handler = self.control_connection.connect(
            self.process_message
        )
        self.blob_connection_handler = self.blob_connection.connect(
            self.process_message
        )

        self.control_connection_handler.send_message(
            message.GetProperties(version=indi.__protocol_version__)
        )

    def onevent(
        self,
        *,
        callback,
        device=None,
        vector=None,
        element=None,
        event_type=events.BaseEvent,
    ):
        uid = uuid.uuid4()
        callback_config = self.CallbackConfig(
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
        uuid=None,
        device=None,
        vector=None,
        element=None,
        event_type=None,
        callback=None,
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
            cb.polling_enabled = False
            self.callbacks.remove(cb)

    def waitforevent(
        self,
        device: str = None,
        vector: str = None,
        element: str = None,
        event_type: Type[events.BaseEvent] = events.BaseEvent,
        expect: Any = None,
        initial: Any = None,
        check: Callable = None,
        timeout: float = -1,
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

        lock = threading.Lock()
        res_event = {}

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

            if release and lock.locked():
                res_event["event"] = event
                lock.release()

        if polling_enabled:

            def poll():
                kwargs = {}
                if device:
                    kwargs["device"] = device
                if vector:
                    kwargs["name"] = vector

                msg = message.GetProperties(version=indi.__protocol_version__, **kwargs)

                time.sleep(polling_delay)
                while lock.locked():
                    self.send_message(msg)
                    time.sleep(polling_interval)

            t = threading.Thread(target=poll)
            t.start()

        lock.acquire()
        uid = self.onevent(
            device=device,
            vector=vector,
            element=element,
            event_type=event_type,
            callback=cb,
        )

        acquired = lock.acquire(timeout=timeout)

        self.rmonevent(uuid=uid)

        if lock.locked():
            lock.release()

        if not acquired:
            raise Exception("Timeout occurred")

        return res_event["event"]

    def trigger_event(self, event: events.BaseEvent):
        for callback in self.callbacks:
            if callback.accepts_event(event):
                try:
                    callback.callback(event)
                except:
                    logger.exception("Error in event handler")
