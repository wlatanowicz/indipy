#!/usr/bin/env python3

import os
from logging import config

from indi.routing import Router
from devices import *
from indi.device.pool import default_pool
from indi.transport.server import TTY as TTYServer

router = Router()

config.dictConfig({
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "verbose": {
                    "format": "[%(asctime)s] %(levelname)s:%(name)s: %(message)s"
                },
            },
            "handlers": {
                "console": {
                    "level": os.environ.get("LOG_LEVEL", "INFO"),
                    "class": "logging.StreamHandler",
                    "formatter": "verbose",
                },
                "indi": {
                    "level": "INFO",
                    "class": "indi.logging.Handler",
                    "formatter": "verbose",
                    "router": router,
                },
            },
            "loggers": {
                "": {
                    "level": "DEBUG",
                    "handlers": ["console", "indi",],
                },
            },
        })

default_pool.init(router)

server = TTYServer(router=router)
server.start()
