import logging

from indi.device import Driver
from indi.message import Message, now
from indi.routing import Router


class Handler(logging.Handler):
    def __init__(self, router: Router, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.router = router

    def emit(self, record):
        timestamp = record.timestamp if hasattr(record, "timestamp") else now()

        device = getattr(record, "device", None)
        if isinstance(device, Driver):
            device = device.name

        msg = Message(device=device, timestamp=timestamp, message=self.format(record))

        self.router.process_message(message=msg)
