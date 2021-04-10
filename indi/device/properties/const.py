from indi.message.const import *


class DriverInterface:
    GENERAL = 0
    TELESCOPE = 1 << 0
    CCD = 1 << 1
    GUIDER = 1 << 2
    FOCUSER = 1 << 3
    FILTER = 1 << 4
    DOME = 1 << 5
    GPS = 1 << 6
    WEATHER = 1 << 7
    AO = 1 << 8
    DUSTCAP = 1 << 9
    LIGHTBOX = 1 << 10
    DETECTOR = 1 << 11
    ROTATOR = 1 << 12
    SPECTROGRAPH = 1 << 13
    CORRELATOR = 1 << 14
    AUX = 1 << 15
