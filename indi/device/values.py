from __future__ import annotations

import base64
import hashlib
import math
import re
from typing import Any


class BLOB:
    def __init__(self, binary: bytes, format: str):
        self.binary = binary
        self.format = format

    @property
    def size(self) -> int:
        return len(self.binary)

    @property
    def binary_base64(self) -> str:
        return base64.b64encode(self.binary).decode("latin1")

    @property
    def md5(self) -> str:
        return hashlib.md5(self.binary).hexdigest()

    @classmethod
    def from_base64(cls, binary_base64: str, format: str) -> BLOB:
        return cls(base64.b64decode(binary_base64), format)

    def __len__(self):
        return self.size


def str_to_num(s: str, fmt: str) -> Any[float, int]:
    if s is None:
        return None
    if not isinstance(s, str):
        s = str(s)

    sexagesimal_match = re.match(r"^%(\d*)\.(\d+)m$", fmt)
    if sexagesimal_match:
        fraction_length = int(sexagesimal_match.groups()[1])
        assert fraction_length in (
            3,
            5,
            6,
            8,
            9,
        ), f"Invalid sexagesimal number format: {fmt}"

        regexps = {
            3: r"^(\-?\d+)[:; ](\d{2})$",
            5: r"^(\-?\d+)[:; ](\d{2}\.\d+)$",
            6: r"^(\-?\d+)[:; ](\d{2})[:; ](\d{2})$",
            8: r"^(\-?\d+)[:; ](\d{2})[:; ](\d{2}.\d+)$",
            9: r"^(\-?\d+)[:; ](\d{2})[:; ](\d{2}.\d+)$",
        }

        num_match = re.match(regexps[fraction_length], s)
        num_match_groups = num_match.groups()
        wholes = num_match_groups[0]
        minutes = num_match_groups[1]
        seconds = num_match_groups[2] if fraction_length in (6, 8, 9) else 0

        return float(wholes) + (float(minutes) / 60) + (float(seconds) / 3600)

    if "." in s:
        return float(s)

    return int(s)


def num_to_str(n: Any[float, int], fmt: str) -> str:
    if n is None:
        return None

    sexagesimal_match = re.match(r"^%(\d*)\.(\d+)m$", fmt)
    if sexagesimal_match:
        fraction_length = int(sexagesimal_match.groups()[1])
        assert fraction_length in (3, 5, 6, 8, 9)

        w = math.floor(n)
        m = (n - w) * 60

        if fraction_length == 3:
            return f"{w}:{m:02.0f}"

        if fraction_length == 5:
            return f"{w}:{m:04.1f}"

        mf = math.floor(m)
        s = (m - mf) * 60
        m = mf

        if fraction_length == 6:
            return f"{w}:{m:02d}:{s:02.0f}"

        if fraction_length == 8:
            return f"{w}:{m:02d}:{s:04.1f}"

        if fraction_length == 9:
            return f"{w}:{m:02d}:{s:05.2f}"

    else:
        return fmt % n
