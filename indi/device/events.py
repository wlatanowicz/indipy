from __future__ import annotations

import asyncio
import uuid
from collections.abc import Callable
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from typing_extensions import Protocol

    from indi.device.driver import Driver
    from indi.device.properties.instance.elements import Element
    from indi.device.properties.instance.vectors import Vector
else:
    Protocol = object

EventCallbackType = Callable[["BaseEvent"], None]


class EventSourceDefinition:
    def __init__(self) -> None:
        self.event_handlers: dict[type[BaseEvent], dict[uuid.UUID, EventCallbackType]] = {}
        super().__init__()

    def attach_event_handler(self, event_type: type[BaseEvent], callback: EventCallbackType) -> uuid.UUID:
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = {}

        uid = uuid.uuid4()
        self.event_handlers[event_type][uid] = callback
        return uid

    def detach_event_handler(self, uid: uuid.UUID):
        for e in self.event_handlers:
            if uid in self.event_handlers[e]:
                del self.event_handlers[e][uid]


class EventSourceProtocol(Protocol):
    @property
    def _definition(self) -> EventSourceDefinition: ...


class EventSource:
    """Mixin used in all event sources (Device, Vector, Element))"""

    def raise_event(self: EventSourceProtocol, event: BaseEvent) -> list[asyncio.Task[None]]:
        event_type = event.__class__
        callbacks = self._definition.event_handlers.get(event_type, {})
        scheduled: list[asyncio.Task[None]] = []

        for _uid, cb in callbacks.items():
            if asyncio.iscoroutinefunction(cb):
                scheduled.append(asyncio.get_running_loop().create_task(cb(event)))
            else:
                cb(event)
        return scheduled


def attach_event_handlers(obj: Driver):
    """Attaches event handlers marked by @on(...) decorator.

    Meant to be used in device definition constuctor.
    Attaches event handlers defined as instance method during definition object initialization.
    It is important to call it at the initialization stage, so `self` argument of event handlers is not broken.

    :param obj: Instance of device definition
    :type obj: object
    """
    for f in [getattr(obj, fn) for fn in dir(obj) if hasattr(obj, fn) and callable(getattr(obj, fn))]:
        if hasattr(f, "event_handler_attachments"):
            attachments = f.event_handler_attachments
            assert isinstance(attachments, list)

            for attachment in attachments:
                assert isinstance(attachment, EventHandlerAttachment)
                attachment.src.attach_event_handler(attachment.event_type, f)


class EventHandlerAttachment:
    def __init__(self, src: EventSourceDefinition, event_type: type[BaseEvent]) -> None:
        self.src = src
        self.event_type = event_type


class _EventHandler(Protocol):
    event_handler_attachments: list[EventHandlerAttachment]

    def __call__(self, event: BaseEvent) -> None: ...


def on(
    src: EventSourceDefinition | list[EventSourceDefinition],
    event_type: type[BaseEvent],
):
    """Decorator with arguments used to mark instance methods as events handlers.

    Marks device definition instance method to bo attached as event handler during device initialization.

    :param src: Event source or list of event sources
    :type src: Union[EventSource, List[EventSource]]
    :param event_type: Event type
    :type event_type: type
    """

    def wrapper(fn: EventCallbackType):
        handler = cast(_EventHandler, fn)
        if not hasattr(handler, "event_handler_attachments"):
            handler.event_handler_attachments = []

        sources = src if isinstance(src, list) else [src]

        for s in sources:
            handler.event_handler_attachments.append(EventHandlerAttachment(s, event_type))

        return fn

    return wrapper


class BaseEvent:
    """Base class for all events."""

    def __init__(
        self,
        device: Driver | None = None,
        vector: Vector | None = None,
        element: Element | None = None,
    ) -> None:
        self.device = device
        self.vector = vector
        self.element = element
        self.prevent_default = False

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, self.__class__)
            and self.__class__ == __value.__class__
            and self.vector == __value.vector
            and self.element == __value.element
            and self.prevent_default == __value.prevent_default
        )


class Write(BaseEvent):
    """Event raised after receiving new value from client.

    Can be used to write new value to physical device.

    Event is raised after a message with new value is received.
    It is not raised after new value is assigned in code.
    To raise this event in code you should use element's
    `set_value` method.

    Set `event.prevent_default` to True to skip the element's internal
    state update. Use that when the device confirms the change later
    and a separate callback assigns the value.

    A normal function must set the flag before it returns. A coroutine
    must set it before its first await. Code after that await cannot
    cancel publication of this client value, and it does not block the
    server read loop.

    If `event.prevent_default` stays False, the state is updated to the
    new value and a `Change` event is raised.
    """

    def __init__(self, element: Element, new_value) -> None:
        super().__init__(element=element, vector=element.vector, device=element.vector.device)
        self.new_value = new_value

    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value) and isinstance(__value, self.__class__) and self.new_value == __value.new_value


class Read(BaseEvent):
    """Event raised before sending value to client.

    Can be used to read value from physical device.

    After the read logic is complete, use `reset_value()` on the element to
    synchronize it's internal state with device's state.
    Don't assign value directly nor use `set_value()` - this will cause infinite recursion.
    """

    def __init__(self, element: Element) -> None:
        super().__init__(element=element, vector=element.vector, device=element.vector.device)


class Change(BaseEvent):
    """Event raised on value change.

    This event is raised after the internal value of element state changes.
    It's raised on both: changes caused by incoming messages and assigns of new values in code.

    It is recommended to use `Read` and `Write` events to communicate with
    physical device.
    """

    def __init__(self, element: Element, old_value, new_value) -> None:
        super().__init__(element=element, vector=element.vector, device=element.vector.device)
        self.new_value = new_value
        self.old_value = old_value

    def __eq__(self, __value: object) -> bool:
        return (
            super().__eq__(__value)
            and isinstance(__value, self.__class__)
            and self.new_value == __value.new_value
            and self.old_value == __value.old_value
        )
