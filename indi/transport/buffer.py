import logging
import xml.etree.ElementTree as ET
from io import StringIO
from typing import Callable, Optional

from indi.message import IndiMessage

logger = logging.getLogger(__name__)


class Buffer:
    def __init__(self) -> None:
        self.max_buffer_size_before_frontal_cleanup: Optional[int] = 2048
        self.buffer = StringIO()
        self.allowed_tags = [m.tag_name() for m in IndiMessage.all_message_classes()]

    def append(self, data: str):
        self.buffer.write(data)

    @property
    def data(self) -> str:
        return self.buffer.getvalue()

    @data.setter
    def data(self, value: str):
        self.buffer = StringIO()
        self.append(value)

    @property
    def data_len(self):
        return self.buffer.tell()

    def _cleanup_buffer(self):
        start = None

        data = self.data
        # find first occurrence of any known xml tag:
        for tag in self.allowed_tags:
            lookup = "<" + tag
            found_pos = data.find(lookup)
            if found_pos >= 0:
                start = min(start, found_pos) if start is not None else found_pos

            if start == 0:
                break

        if start is not None:
            if start > 0:
                self.data = data[start:]
            return

        # if no known tags found
        # search for the last xml tag opening
        # just in case it's the part of valid message
        # and the rest will arrive soon
        last_tag_pos = data.rfind("<")
        if last_tag_pos >= 0:
            start = last_tag_pos

        if start is not None:
            if start > 0:
                self.data = data[start:]
            return

        # neither known tag nor xml opening found in the buffer
        # we can safely assume everything is junk and discard it
        self.data = ""

    def _cleanup_beginning(self):
        self.data = self.data[1:]
        self._cleanup_buffer()

    def _find_message_in_buffer(self):
        end = 0
        data = self.data
        while end < len(data) - 1:
            end = data.find(">", end)
            if end < 0:
                return None, None

            end += 1

            partial = data[:end]

            try:
                ET.fromstring(partial)
                is_correct_xml = True
            except ET.ParseError:
                is_correct_xml = False

            if is_correct_xml:
                try:
                    message = IndiMessage.from_string(partial)
                    return message, end
                except Exception:
                    logger.warning("Buffer: Contents is not a valid message")
        return None, None

    def process(self, callback: Callable[[IndiMessage], None]):
        self._cleanup_buffer()
        while self.data_len:
            message, end = self._find_message_in_buffer()

            if not message and self.max_buffer_size_before_frontal_cleanup is not None:
                if self.data_len > self.max_buffer_size_before_frontal_cleanup:
                    self._cleanup_beginning()
                    continue
                break

            self.data = self.data[end:]
            self._cleanup_buffer()
            callback(message)
