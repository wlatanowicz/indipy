import logging
import xml.etree.ElementTree as ET

from indi.message import IndiMessage


class Buffer:
    def __init__(self):
        self.data = ""

        self.allowed_tags = [m.tag_name() for m in IndiMessage.__all_subclasses__()]

    def append(self, data):
        self.data += data

    def _cleanup_buffer(self):
        start = len(self.data) - 1
        for tag in self.allowed_tags:
            start = min(start, self.data.find("<" + tag))

        if start >= 0:
            self.data = self.data[start:]

    def process(self, callback):
        self._cleanup_buffer()
        end = 0
        while len(self.data) > 0 and end >= 0:
            end = self.data.find(">", end)

            if end > 0:
                end += 1
                partial = self.data[0:end]

                try:
                    xml = ET.fromstring(partial)
                    self.data = self.data[end:]
                    end = 0
                    message = None
                    try:
                        message = IndiMessage.from_string(partial)
                    except Exception as ex:
                        logging.warning("Buffer: Contents is not a valid message")

                    if message:
                        try:
                            callback(message)
                        except:
                            logging.exception("Error procesing message")
                except ET.ParseError:
                    pass
