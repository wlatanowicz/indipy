import os
import asyncio
from logging import config

from indi.client import elements
from indi.client.client import Client
from indi.message import const
from indi.transport.client import TCP


def configure_logging():
    config.dictConfig(
        {
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
            },
            "loggers": {
                "": {
                    "level": "DEBUG",
                    "handlers": [
                        "console",
                    ],
                },
            },
        }
    )


async def main_loop():
    host = os.environ.get("INDISERVER_HOST", "indiserver")
    port = int(os.environ.get("INDISERVER_PORT", 7624))

    control_connection = TCP(host, port)
    blob_connection = TCP(host, port)

    async def client_callback(event):
        print(event)

    client = Client(control_connection, blob_connection)
    client.onevent(callback=client_callback)

    await client.start()

    while True:
        await asyncio.sleep(100)


if __name__ == "__main__":
    configure_logging()
    asyncio.run(main_loop())
