import logging
import asyncio

from indi.device import Driver, properties
from indi.device.pool import default_pool
from indi.message import const
from indi.device.properties.const import DriverInterface
from indi.device.properties import standard
from indi.device.events import on, Write

logger = logging.getLogger(__name__)


max_position = 5000


@default_pool.register
class FocuserSimulator(Driver):
    name = "Python Focuser Simulator"

    general = properties.Group(
        "GENERAL",
        vectors=dict(
            connection=standard.common.Connection(),
            driver_info=standard.common.DriverInfo(
                interface=(DriverInterface.FOCUSER,)
            ),
            info=properties.TextVector(
                "INFO",
                enabled=False,
                perm=const.Permissions.READ_ONLY,
                elements=dict(
                    manufacturer=properties.Text("MANUFACTURER", default="INDIpy"),
                    camera_model=properties.Text(
                        "FOCUSER_MODEL", default="FocuserSimulator"
                    ),
                ),
            ),
        ),
    )

    position = properties.Group(
        "POSITION",
        enabled=False,
        vectors=dict(
            position=standard.focuser.AbsolutePosition(min=0, max=max_position, step=1),
            motion=standard.focuser.FocusMotion(),
            rel_position=standard.focuser.RelativePosition(),
            fmax=standard.focuser.FocusMax(default=max_position),
        ),
    )

    @on(general.connection.connect, Write)
    async def connect(self, event):
        value = event.new_value
        connected = value == const.SwitchState.ON
        self.general.connection.state_ = const.State.BUSY

        if connected:
            try:
                self.position.position.position.reset_value(0)
                self.general.connection.state_ = const.State.OK
            except Exception as e:
                self.general.connection.state_ = const.State.ALERT
                connected = False
                logger.error(e)

        self.general.connection.connect.bool_value = connected
        self.position.enabled = connected
        self.general.info.enabled = connected

    @on(position.position.position, Write)
    async def reposition(self, event):
        value = event.new_value
        await self._move(value)

    @on(position.rel_position.position, Write)
    async def step(self, event):
        value = event.new_value
        self.position.rel_position.position.state_ = const.State.BUSY
        current_position = self.position.position.position.value
        direction = 1 if self.position.motion.outward.bool_value else -1
        new_value = current_position + direction * value
        await self._move(new_value)
        self.position.rel_position.position.state_ = const.State.OK

    async def _move(self, target):
        self.position.position.state_ = const.State.BUSY
        start_position = self.position.position.position.value
        step_size = 20
        direction = 1 if target > start_position else -1

        while abs(float(self.position.position.position.value) - float(target)) > 0.01:
            await asyncio.sleep(1)
            self.position.position.position.value += step_size * direction

        self.position.position.state_ = const.State.OK
