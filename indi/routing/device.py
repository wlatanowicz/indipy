from indi.message import IndiMessage


class Device:
    def message_from_client(self, message: IndiMessage):
        raise Exception("Not implemented")

    def accepts(self, device: str | None) -> bool:
        raise Exception("Not implemented")
