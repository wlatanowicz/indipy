import logging

from indi.device.pool import DevicePool
from indi.routing import Router
from indi.transport.server import TCP as TCPServer

from devices import *


logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

router = Router()

DevicePool.init(router)

server = TCPServer(router=router)
server.start()
