import os
import asyncio
from logging import config

from indi.client import elements
from indi.client.client import Client
from indi.message import const
from indi.transport.client import TCP

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
                    "level": os.environ.get("LOG_LEVEL", "DEBUG"),
                    "class": "logging.StreamHandler",
                    "formatter": "verbose",
                },
            },
            "loggers": {
                "": {
                    "level": "DEBUG",
                    "handlers": ["console",],
                },
            },
        })

host = os.environ.get("INDISERVER_HOST", "indiserver")
port = int(os.environ.get("INDISERVER_PORT", 7624))

control_connection = TCP(host, port)
blob_connection = TCP(host, port)

def client_callback(event):
    print(event)


client = Client(control_connection, blob_connection)
client.onevent(callback=client_callback)

async def main_loop():
    asyncio.get_running_loop().create_task(client.start())
    while True:
        await asyncio.sleep(100)


asyncio.run(main_loop())
