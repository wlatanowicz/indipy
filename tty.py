#!/usr/bin/env python3

import logging

from devices import *
from indi.device.pool import DevicePool
from indi.routing import Router
from indi.transport.server import TTY as TTYServer

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

router = Router()

DevicePool.init(router)

server = TTYServer(router=router)
server.start()
