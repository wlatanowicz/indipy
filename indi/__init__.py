from os import path


with open(path.join(path.dirname(__file__), "VERSION")) as f:
    __version__ = f.read().strip()

__protocol_version__ = "1.7"

__author__ = "Wiktor Latanowicz"
