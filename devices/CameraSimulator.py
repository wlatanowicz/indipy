import threading
import time

from indi.device import Driver, properties
from indi.message import const
from indi.device.pool import DevicePool


@DevicePool.register
class CameraSimulator(Driver):

    name = "CAMERA_SIMULATOR"

    general = properties.Group(
        "GENERAL",
        vectors=dict(
            connection=properties.Standard("CONNECTION", onchange="connect"),
            active_device=properties.Standard(
                "ACTIVE_DEVICES",
                elements=dict(camera=properties.Text("ACTIVE_CCD", default=name)),
            ),
        ),
    )

    settings = properties.Group(
        "SETTINGS",
        enabled=False,
        vectors=dict(
            upload_mode=properties.Standard("UPLOAD_MODE", default_on="UPLOAD_LOCAL"),
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
        vectors=dict(exposure=properties.Standard("CCD_EXPOSURE")),
    )
    exposition.exposure.time.onwrite = "expose"

    def connect(self, sender):
        connected = sender.connect.bool_value
        self.exposition.enabled = connected
        self.settings.enabled = connected

    def expose(self, sender):
        def worker():
            print(f"EXPOSE for {self.exposition.exposure.time.value}!!!!!")
            self.exposition.exposure.state_ = const.State.BUSY
            time.sleep(int(float(self.exposition.exposure.time.value)))
            self.exposition.exposure.state_ = const.State.OK
            print(f"FINISHED EXPOSE for {self.exposition.exposure.time.value}!!!!!")

        w = threading.Thread(name="worker", target=worker)
        w.start()
