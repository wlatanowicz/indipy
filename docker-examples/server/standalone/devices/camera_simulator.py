import threading
import time
import logging

from indi.device import Driver, properties
from indi.device.pool import default_pool
from indi.device.properties import const
from indi.device.properties.const import DriverInterface
from indi.device.properties import standard
from indi.device.events import on, Write, Change
import asyncio

logger = logging.getLogger(__name__)


@default_pool.register
class CameraSimulator(Driver):

    name = "CAMERA_SIMULATOR"

    general = properties.Group(
        "GENERAL",
        vectors=dict(
            connection=standard.common.Connection(),
            driver_info = standard.common.DriverInfo(interface=(DriverInterface.CCD,)),
        ),
    )

    settings = properties.Group(
        "SETTINGS",
        enabled=False,
        vectors=dict(
            upload_mode=standard.ccd.UploadMode(),
            iso=properties.SwitchVector(
                "ISO",
                rule=properties.SwitchVector.RULES.ONE_OF_MANY,
                default_on="100",
                elements=dict(
                    iso100=properties.Switch("100"),
                    iso200=properties.Switch("200"),
                    iso400=properties.Switch("400"),
                ),
            ),
        ),
    )

    exposition = properties.Group(
        "EXPOSITION",
        enabled=False,
        vectors=dict(
            exposure=standard.ccd.Exposure()
        ),
    )

    @on(general.connection.connect, Change)
    async def connect(self, event):
        connected = self.general.connection.connect.bool_value
        self.exposition.enabled = connected
        self.settings.enabled = connected
        client = self.snoop_device("CCD Simulator", "FILTER_SLOT")

        def clb(event):
            logger.info("Snooped event: %s", event)

        client.onevent(callback=clb)

    @on(exposition.exposure.time, Write)
    async def expose(self, event):
        value = event.new_value
        logger.info(f"EXPOSE for {value}!!!!!", extra={"device": self})
        time_left = value
        self.exposition.exposure.state_ = const.State.BUSY
        while time_left > 0:
            self.exposition.exposure.time.value = time_left
            await asyncio.sleep(0.1)
            time_left -= 0.1
        self.exposition.exposure.state_ = const.State.OK
        logger.info(f"FINISHED EXPOSE for {value}!!!!!", extra={"device": self})
