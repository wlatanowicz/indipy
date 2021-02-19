import os
from indi.client import elements
from indi.client.client import Client
from indi.message import const
from indi.transport.client import TCP
import hashlib

from indi.message.const import SwitchState, State
import time


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


host = os.environ.get("INDISERVER_HOST", "indiserver")
port = int(os.environ.get("INDISERVER_PORT", 7624))

control_connection = TCP(host, port)
blob_connection = TCP(host, port)

client = Client(control_connection, blob_connection)
client.start()


client.waitforevent(
    device="CCD Simulator",
    vector="CONNECTION",
    element="CONNECT",
    check=lambda _: True
)

client.waitforevent(
    device="Focuser Simulator",
    vector="CONNECTION",
    element="CONNECT",
    check=lambda _: True
)

client.waitforevent(
    device="Telescope Simulator",
    vector="CONNECTION",
    element="CONNECT",
    check=lambda _: True
)

client["CCD Simulator"]["CONNECTION"]["CONNECT"].value = SwitchState.ON
client["CCD Simulator"]["CONNECTION"].submit()

client["Focuser Simulator"]["CONNECTION"]["CONNECT"].value = SwitchState.ON
client["Focuser Simulator"]["CONNECTION"].submit()

client["Telescope Simulator"]["CONNECTION"]["CONNECT"].value = SwitchState.ON
client["Telescope Simulator"]["CONNECTION"].submit()

client.waitforevent(
    device="CCD Simulator",
    vector="CONNECTION",
    element="CONNECT",
    check=lambda e: e.element.value == SwitchState.ON and e.vector.state == State.OK
)

client.waitforevent(
    device="Focuser Simulator",
    vector="CONNECTION",
    element="CONNECT",
    check=lambda e: e.element.value == SwitchState.ON and e.vector.state == State.OK
)

client.waitforevent(
    device="Telescope Simulator",
    vector="CONNECTION",
    element="CONNECT",
    check=lambda e: e.element.value == SwitchState.ON and e.vector.state == State.OK
)

pos = 20000

client["Focuser Simulator"]["ABS_FOCUS_POSITION"]["FOCUS_ABSOLUTE_POSITION"].value = pos
client["Focuser Simulator"]["ABS_FOCUS_POSITION"].submit()

client.waitforevent(
    device="Focuser Simulator",
    vector="ABS_FOCUS_POSITION",
    element="FOCUS_ABSOLUTE_POSITION",
    check=lambda e: e.new_value == pos and e.vector.state == State.OK
)

for d in client.list_devices():
    print(d)
    for v in client[d].list_vectors():
        ve = client[d][v]
        print(f"  - {v} <{ve.__class__.__name__}> ?= {ve.state}")
        for e in client[d][v].list_elements():
            el = client[d][v][e]
            print(f"    = {e} <{el.__class__.__name__}> == {el.value}")


while True:
    expose = 5.0

    client["CCD Simulator"]["CCD_EXPOSURE"]["CCD_EXPOSURE_VALUE"].value = expose
    client["CCD Simulator"]["CCD_EXPOSURE"].submit()

    client.waitforevent(
        device="CCD Simulator",
        vector="CCD_EXPOSURE",
        check=lambda e: e.vector.state == State.OK
    )
    initial = client["CCD Simulator"]["CCD1"]["CCD1"].value
    event = client.waitforevent(
        device="CCD Simulator",
        vector="CCD1",
        element="CCD1",
        check=lambda e: e.new_value != initial and e.new_value is not None,
    )

    blob = event.element.value
    size = sizeof_fmt(len(blob))

    print(f"Got new image blob size={size} md5={blob.md5} format={blob.format}")

    time.sleep(5)
