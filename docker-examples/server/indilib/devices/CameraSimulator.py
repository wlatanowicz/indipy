import threading
import time
import logging

from indi.device import Driver, properties
from indi.device.pool import default_pool
from indi.device.properties import const
from indi.device.properties.const import DriverInterface
from indi.device.properties import standard

logger = logging.getLogger(__name__)


@default_pool.register
class CameraSimulator(Driver):

    name = "CAMERA_SIMULATOR"

    general = properties.Group(
        "GENERAL",
        vectors=dict(
            connection=standard.common.Connection(onchange="connect"),
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
    exposition.exposure.time.onwrite = "expose"

    def connect(self, sender):
        connected = self.general.connection.connect.bool_value
        self.exposition.enabled = connected
        self.settings.enabled = connected

    def expose(self, sender, value):
        def worker():
            logger.info(f"EXPOSE for {value}!!!!!", extra={"device": self})
            self.exposition.exposure.time.value = value
            self.exposition.exposure.state_ = const.State.BUSY
            time.sleep(float(value))
            self.exposition.exposure.state_ = const.State.OK
            logger.info(f"FINISHED EXPOSE for {value}!!!!!", extra={"device": self})

        w = threading.Thread(name="worker", target=worker)
        w.start()
