import threading
import time
import uuid
from typing import Any

from indi import message
from indi.client.device import Device
from indi.client.elements import Element
from indi.client.vectors import Vector
from indi.message import IndiMessage, const


class Client:
    def __init__(self, control_connection, blob_connection):
        self.devices = {}
        self.control_connection = control_connection
        self.blob_connection = blob_connection
        self.control_connection_handler = None
        self.blob_connection_handler = None
        self.callbacks = []

    def __getitem__(self, key) -> Device:
        return self.devices[key]

    def __contains__(self, key) -> bool:
        return key in self.devices

    def get_device(self, name: str) -> Device:
        return self.devices.get(name)

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
            message.GetProperties(version="2.0")
        )

    def onupdate(
        self, *, callback, device=None, vector=None, element=None, what="value"
    ):
        uid = uuid.uuid4()
        callback_config = dict(
            what=what,
            device=device,
            vector=vector,
            element=element,
            callback=callback,
            uuid=uid,
        )

        self.callbacks.append(callback_config)
        return uid

    def rmonupdate(
        self,
        uuid=None,
        device=None,
        vector=None,
        element=None,
        what=None,
        callback=None,
    ):
        to_rm = list()
        for cb in self.callbacks:
            if (
                uuid in (None, cb["uuid"],)
                and device in (None, cb["device"],)
                and vector in (None, cb["vector"],)
                and element in (None, cb["element"],)
                and what in (None, cb["what"],)
                and callback in (None, cb["callback"])
            ):
                to_rm.append(cb)

        for cb in to_rm:
            cb["polling_enabled"] = False
            self.callbacks.remove(cb)

    def waitforupdate(
        self,
        device=None,
        vector=None,
        element=None,
        what=None,
        expect=None,
        initial=None,
        cmp=None,
        timeout=-1,
        polling_enabled=True,
        polling_delay=1.0,
        polling_interval=1.0,
    ):
        if cmp is None:
            cmp = lambda a, b: a == b

        lock = threading.Lock()

        def cb(sender, **kwargs):
            release = False

            if expect is None:
                if initial is None:
                    release = True
                elif initial != sender.value:
                    release = True
            else:
                try:
                    if what == "state" and cmp(sender.state, expect):
                        release = True
                except AttributeError:
                    pass

                try:
                    if what == "value" and cmp(sender.value, expect):
                        release = True
                except AttributeError:
                    pass

            if release and lock.locked():
                lock.release()

        if polling_enabled:

            def poll():
                kwargs = {}
                if device:
                    kwargs["device"] = device
                if vector:
                    kwargs["name"] = vector

                msg = message.GetProperties(version="2.0", **kwargs)

                time.sleep(polling_delay)
                while lock.locked():
                    self.send_message(msg)
                    time.sleep(polling_interval)

            t = threading.Thread(target=poll)
            t.start()

        lock.acquire()
        uid = self.onupdate(
            device=device, vector=vector, element=element, what=what, callback=cb
        )

        acquired = lock.acquire(timeout=timeout)

        self.rmonupdate(uuid=uid)

        if lock.locked():
            lock.release()

        if not acquired:
            raise Exception("Timeout occurred")

    def trigger_update(self, sender: Any[Element, Vector], what, **kwargs):
        sender_device = None
        sender_vector = None
        sender_element = None

        if isinstance(sender, Element):
            sender_device = sender.vector.device.name
            sender_vector = sender.vector.name
            sender_element = sender.name
        elif isinstance(sender, Vector):
            sender_device = sender.device.name
            sender_vector = sender.name

        for callback in self.callbacks:
            if (
                callback["device"] in (None, sender_device,)
                and callback["vector"] in (None, sender_vector,)
                and callback["element"] in (None, sender_element,)
                and callback["what"] in (None, what,)
            ):

                callback["callback"](sender, what=what, **kwargs)
