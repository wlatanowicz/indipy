from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Union, Type, Callable

if TYPE_CHECKING:
    from indi.device.driver import Device
    from indi.device.properties.instance.elements import Element
    from indi.device.properties.instance.vectors import Vector


class EventSourceDefinition:
    def __init__(self):
        self.event_handlers = {}
        super().__init__()

    def attach_event_handler(
        self, event_type: Type[BaseEvent], callback: Callable
    ) -> uuid:
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = {}

        uid = uuid.uuid4()
        self.event_handlers[event_type][uid] = callback
        return uid

    def detach_event_handler(self, uid: uuid):
        for e in self.event_handlers:
            if uid in self.event_handlers[e]:
                del self.event_handlers[e][uid]


class EventSource:
    """Mixin used in all event sources (Device, Vector, Element))"""

    def raise_event(self, event: BaseEvent):
        event_type = event.__class__
        callbacks = self._definition.event_handlers.get(event_type, {})

        for uid, cb in callbacks.items():
            cb(event)


def attach_event_handlers(obj):
    """Attaches event handlers marked by @on(...) decorator.

    Meant to be used in device definition constuctor.
    Attaches event handlers defined as instance method during definition object initialization.
    It is important to call it at the initialization stage, so `self` argument of event handlers is not broken.

    :param obj: Instance of device definition
    :type obj: object
    """
    for f in [
        getattr(obj, fn)
        for fn in dir(obj)
        if hasattr(obj, fn) and callable(getattr(obj, fn))
    ]:
        if hasattr(f, "event_handler_attachments"):
            attachments = f.event_handler_attachments
            assert isinstance(attachments, list)

            for attachment in attachments:
                assert isinstance(attachment, EventHandlerAttachment)
                attachment.src.attach_event_handler(attachment.event_type, f)


class EventHandlerAttachment:
    def __init__(self, src: EventSource, event_type: type):
        self.src = src
        self.event_type = event_type


def on(src: Union[EventSource, List[EventSource]], event_type: type):
    """Decorator with arguments used to mark instance methods as events handlers.

    Marks device definition instance method to bo attached as event handler during device initialization.

    :param src: Event source or list of event sources
    :type src: Union[EventSource, List[EventSource]]
    :param event_type: Event type
    :type event_type: type
    """

    def wrapper(fn):
        if not hasattr(fn, "event_handler_attachments"):
            fn.event_handler_attachments = []

        if isinstance(src, list):
            sources = src
        else:
            sources = [src]

        for s in sources:
            fn.event_handler_attachments.append(EventHandlerAttachment(s, event_type))

        return fn

    return wrapper


class BaseEvent:
    """Base class for all events."""

    def __init__(
        self, device: Driver = None, vector: Vector = None, element: Element = None
    ):
        self.device = device
        self.vector = vector
        self.element = element
        self.prevent_default = False
        self.propagate = True


class Write(BaseEvent):
    """Event raised after receiving new value from client.

    Can be used to write new value to physical device.
    """

    def __init__(self, element: Element, new_value):
        super().__init__(
            element=element, vector=element.vector, device=element.vector.device
        )
        self.new_value = new_value


class Read(BaseEvent):
    """Event raised before sending value to client.

    Can be used to read value from physical device.
    """

    def __init__(self, element: Element):
        super().__init__(
            element=element, vector=element.vector, device=element.vector.device
        )


class Change(BaseEvent):
    """Event raised on value change."""

    def __init__(self, element: Element, old_value, new_value):
        super().__init__(
            element=element, vector=element.vector, device=element.vector.device
        )
        self.new_value = new_value
        self.old_value = new_value
