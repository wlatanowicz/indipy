from typing import Optional

from indi.client.client import BaseClient
from indi.message import IndiMessage
from indi.routing.client import Client as RoutingClient
from indi.routing.router import Router


class SnoopingClient(BaseClient, RoutingClient):
    def __init__(self, router: Optional[Router]) -> None:
        super().__init__()
        self.router = router

    def send_message(self, msg: IndiMessage):
        if msg and self.router:
            self.router.process_message(msg, self)

    def message_from_device(self, message: IndiMessage):
        self.process_message(message)
