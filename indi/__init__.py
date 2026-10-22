from pathlib import Path

with (Path(__file__).parent / "VERSION").open() as version_file:
    __version__ = version_file.read().strip()

__protocol_version__ = "1.7"

__author__ = "Wiktor Latanowicz"
