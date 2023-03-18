from typing import Optional

from indi.client.client import BaseClient
from indi.message import IndiMessage
from indi.routing.router import Router


class SnoopingClient(BaseClient):
    def __init__(self, router):
        super().__init__()
        self.router: Optional[Router] = router

    def send_message(self, msg: IndiMessage):
        if msg and self.router:
            self.router.process_message(msg, self)

    def message_from_device(self, message):
        self.process_message(message)
