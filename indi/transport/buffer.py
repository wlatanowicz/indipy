import logging
import xml.etree.ElementTree as ET
from typing import Callable

from indi.message import IndiMessage

logger = logging.getLogger(__name__)


class Buffer:
    def __init__(self) -> None:
        self.data = ""
        self.allowed_tags = [m.tag_name() for m in IndiMessage.__all_subclasses__()]

    def append(self, data: str):
        self.data += data

    def _cleanup_buffer(self):
        start = None

        # find first occurrence of any known xml tag:
        for tag in self.allowed_tags:
            lookup = "<" + tag
            found_pos = self.data.find(lookup)
            if found_pos >= 0:
                start = min(start, found_pos) if start is not None else found_pos

            if start == 0:
                break

        if start is not None:
            if start > 0:
                self.data = self.data[start:]
            return

        # if no known tags found
        # search for the last xml tag opening
        # just in case it's the part of valid message
        # and the rest will arrive soon
        last_tag_pos = self.data.rfind("<")
        if last_tag_pos >= 0:
            start = last_tag_pos

        if start is not None:
            if start > 0:
                self.data = self.data[start:]
            return

        # neither known tag nor xml opening found in the buffer
        # we can safely assume everything is junk and discard it
        self.data = ""

    def _cleanup_beginning(self):
        self.data = self.data[1:]
        self._cleanup_buffer()

    def _find_message_in_buffer(self):
        end = 0
        while end < len(self.data) - 1:
            end = self.data.find(">", end)
            if end < 0:
                return None, None

            end += 1

            partial = self.data[:end]

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
        while self.data:
            message, end = self._find_message_in_buffer()
            if not message:
                if len(self.data) > 1024:
                    self._cleanup_beginning()
                    continue
                break

            self.data = self.data[end:]
            self._cleanup_buffer()
            callback(message)
