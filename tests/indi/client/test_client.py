import indi
from indi import message
from indi.client.client import Client
from indi.device import Driver, properties, values
from indi.message import IndiMessage
from indi.routing import Client as RoutingClient
from indi.routing import Router


class Camera(Driver):
    name = "CAMERA"

    main = properties.Group(
        "MAIN",
        vectors={
            "exposure": properties.NumberVector(
                "EXPOSURE",
                elements={
                    "seconds": properties.Number("SECONDS", default=1),
                },
            ),
            "image": properties.BLOBVector(
                "IMAGE",
                elements={
                    "fits": properties.BLOB("FITS"),
                },
            ),
        },
    )


class Loopback(RoutingClient):
    def __init__(self, router: Router, client: Client, outbound: list[tuple[RoutingClient, IndiMessage]]):
        self.router = router
        self.client = client
        self.outbound = outbound
        router.register_client(self)

    def send_message(self, msg: IndiMessage):
        self.outbound.append((self, msg))

    def message_from_device(self, msg: IndiMessage):
        self.client.process_message(msg)


def test_blob_connection_learns_definitions_before_updates():
    router = Router()
    driver = Camera(router=router)
    outbound: list[tuple[RoutingClient, IndiMessage]] = []
    client = Client(None, None)
    control = Loopback(router, client, outbound)
    blob = Loopback(router, client, outbound)
    client.control_connection_handler = control
    client.blob_connection_handler = blob

    control.send_message(message.GetProperties(version=indi.__protocol_version__))
    while outbound:
        sender, msg = outbound.pop(0)
        router.process_message(msg, sender=sender)

    image = client["CAMERA"]["IMAGE"]
    assert image["FITS"].value is None

    driver.main.image.fits.value = values.BLOB(binary=b"pixels", format=".fits")

    assert image["FITS"].value.binary == b"pixels"
