import pytest

from indi.device import properties
from indi.device.properties import const
from indi.device.properties.standard import ccd, common, dome, filterwheel, focuser, telescope

_INFO_MEMBERS = (
    "CCD_MAX_X",
    "CCD_MAX_Y",
    "CCD_PIXEL_SIZE",
    "CCD_PIXEL_SIZE_X",
    "CCD_PIXEL_SIZE_Y",
    "CCD_BITSPERPIXEL",
)
_TRACK_MODES = ("TRACK_SIDEREAL", "TRACK_SOLAR", "TRACK_LUNAR")
_MEASUREMENT_TAIL = (
    "DM_NORTH_DISPLACEMENT",
    "DM_EAST_DISPLACEMENT",
    "DM_UP_DISPLACEMENT",
    "DM_OTA_OFFSET",
)

CASES = [
    (common.DevicePort, properties.TextVector, "DEVICE_PORT", ("PORT",)),
    (common.TimeLst, properties.NumberVector, "TIME_LST", ("LST",)),
    (common.TimeUtc, properties.TextVector, "TIME_UTC", ("UTC", "OFFSET")),
    (common.GeographicCoord, properties.NumberVector, "GEOGRAPHIC_COORD", ("LAT", "LONG", "ELEV")),
    (common.Atmosphere, properties.NumberVector, "ATMOSPHERE", ("TEMPERATURE", "PRESSURE", "HUMIDITY")),
    (common.UploadSettings, properties.TextVector, "UPLOAD_SETTINGS", ("UPLOAD_DIR", "UPLOAD_PREFIX")),
    (telescope.EquatorialCoord, properties.NumberVector, "EQUATORIAL_COORD", ("RA", "DEC")),
    (telescope.EquatorialEodCoord, properties.NumberVector, "EQUATORIAL_EOD_COORD", ("RA", "DEC")),
    (telescope.TargetEodCoord, properties.NumberVector, "TARGET_EOD_COORD", ("RA", "DEC")),
    (telescope.HorizontalCoord, properties.NumberVector, "HORIZONTAL_COORD", ("ALT", "AZ")),
    (telescope.OnCoordSet, properties.SwitchVector, "ON_COORD_SET", ("SLEW", "TRACK", "SYNC")),
    (telescope.TelescopeMotionNS, properties.SwitchVector, "TELESCOPE_MOTION_NS", ("MOTION_NORTH", "MOTION_SOUTH")),
    (telescope.TelescopeMotionWE, properties.SwitchVector, "TELESCOPE_MOTION_WE", ("MOTION_WEST", "MOTION_EAST")),
    (
        telescope.TelescopeTimedGuideNS,
        properties.NumberVector,
        "TELESCOPE_TIMED_GUIDE_NS",
        ("TIMED_GUIDE_N", "TIMED_GUIDE_S"),
    ),
    (
        telescope.TelescopeTimedGuideWE,
        properties.NumberVector,
        "TELESCOPE_TIMED_GUIDE_WE",
        ("TIMED_GUIDE_W", "TIMED_GUIDE_E"),
    ),
    (
        telescope.TelescopeSlewRate,
        properties.SwitchVector,
        "TELESCOPE_SLEW_RATE",
        ("SLEW_GUIDE", "SLEW_CENTERING", "SLEW_FIND", "SLEW_MAX"),
    ),
    (telescope.TelescopePark, properties.SwitchVector, "TELESCOPE_PARK", ("PARK", "UNPARK")),
    (telescope.TelescopeParkPosition, properties.NumberVector, "TELESCOPE_PARK_POSITION", ("PARK_RA", "PARK_DEC")),
    (
        telescope.TelescopeParkOption,
        properties.SwitchVector,
        "TELESCOPE_PARK_OPTION",
        ("PARK_CURRENT", "PARK_DEFAULT", "PARK_WRITE_DATA"),
    ),
    (telescope.TelescopeAbortMotion, properties.SwitchVector, "TELESCOPE_ABORT_MOTION", ("ABORT_MOTION",)),
    (telescope.TelescopeTrackRate, properties.SwitchVector, "TELESCOPE_TRACK_RATE", _TRACK_MODES),
    (telescope.TelescopeTrackMode, properties.SwitchVector, "TELESCOPE_TRACK_MODE", _TRACK_MODES),
    (
        telescope.TelescopeAxisTrackRate,
        properties.NumberVector,
        "TELESCOPE_TRACK_RATE",
        ("TRACK_RATE_RA", "TRACK_RATE_DE"),
    ),
    (
        telescope.TelescopeInfo,
        properties.NumberVector,
        "TELESCOPE_INFO",
        ("TELESCOPE_APERTURE", "TELESCOPE_FOCAL_LENGTH", "GUIDER_APERTURE", "GUIDER_FOCAL_LENGTH"),
    ),
    (telescope.TelescopePierSide, properties.SwitchVector, "TELESCOPE_PIER_SIDE", ("PIER_EAST", "PIER_WEST")),
    (ccd.AbortExposure, properties.SwitchVector, "CCD_ABORT_EXPOSURE", ("ABORT",)),
    (ccd.Frame, properties.NumberVector, "CCD_FRAME", ("X", "Y", "WIDTH", "HEIGHT")),
    (ccd.Temperature, properties.NumberVector, "CCD_TEMPERATURE", ("CCD_TEMPERATURE_VALUE",)),
    (ccd.Cooler, properties.SwitchVector, "CCD_COOLER", ("COOLER_ON", "COOLER_OFF")),
    (ccd.CoolerPower, properties.NumberVector, "CCD_COOLER_POWER", ("CCD_COOLER_VALUE",)),
    (
        ccd.FrameType,
        properties.SwitchVector,
        "CCD_FRAME_TYPE",
        ("FRAME_LIGHT", "FRAME_BIAS", "FRAME_DARK", "FRAME_FLAT"),
    ),
    (ccd.Binning, properties.NumberVector, "CCD_BINNING", ("HOR_BIN", "VER_BIN")),
    (ccd.Compression, properties.SwitchVector, "CCD_COMPRESSION", ("INDI_ENABLED", "INDI_DISABLED")),
    (ccd.FrameReset, properties.SwitchVector, "CCD_FRAME_RESET", ("RESET",)),
    (ccd.Info, properties.NumberVector, "CCD_INFO", _INFO_MEMBERS),
    (ccd.Cfa, properties.TextVector, "CCD_CFA", ("CFA_OFFSET_X", "CFA_OFFSET_Y", "CFA_TYPE")),
    (ccd.Image, properties.BLOBVector, "CCD1", ("CCD1",)),
    (ccd.GuiderExposure, properties.NumberVector, "GUIDER_EXPOSURE", ("GUIDER_EXPOSURE_VALUE",)),
    (ccd.VideoStream, properties.SwitchVector, "CCD_VIDEO_STREAM", ("STREAM_ON", "STREAM_OFF")),
    (
        ccd.StreamingExposure,
        properties.NumberVector,
        "STREAMING_EXPOSURE",
        ("STREAMING_EXPOSURE_VALUE", "STREAMING_DIVISOR_VALUE"),
    ),
    (ccd.Fps, properties.NumberVector, "FPS", ("EST_FPS", "AVG_FPS")),
    (ccd.RecordFile, properties.TextVector, "RECORD_FILE", ("RECORD_FILE_DIR", "RECORD_FILE_NAME")),
    (ccd.RecordOptions, properties.NumberVector, "RECORD_OPTIONS", ("RECORD_DURATION", "RECORD_FRAME_TOTAL")),
    (
        ccd.RecordStream,
        properties.SwitchVector,
        "RECORD_STREAM",
        ("RECORD_ON", "RECORD_DURATION_ON", "RECORD_FRAME_ON", "RECORD_OFF"),
    ),
    (filterwheel.FilterSlot, properties.NumberVector, "FILTER_SLOT", ("FILTER_SLOT_VALUE",)),
    (filterwheel.FilterName, properties.TextVector, "FILTER_NAME", ("FILTER_NAME_VALUE",)),
    (focuser.FocusSpeed, properties.NumberVector, "FOCUS_SPEED", ("FOCUS_SPEED_VALUE",)),
    (focuser.FocusTimer, properties.NumberVector, "FOCUS_TIMER", ("FOCUS_TIMER_VALUE",)),
    (focuser.FocusReverseMotion, properties.SwitchVector, "FOCUS_REVERSE_MOTION", ("ENABLED", "DISABLED")),
    (
        focuser.FocusReverseMotionIndi,
        properties.SwitchVector,
        "FOCUS_REVERSE_MOTION",
        ("INDI_ENABLED", "INDI_DISABLED"),
    ),
    (focuser.FocusAbortMotion, properties.SwitchVector, "FOCUS_ABORT_MOTION", ("ABORT",)),
    (focuser.FocusSync, properties.NumberVector, "FOCUS_SYNC", ("FOCUS_SYNC_VALUE",)),
    (dome.DomeSpeed, properties.NumberVector, "DOME_SPEED", ("DOME_SPEED_VALUE",)),
    (dome.DomeMotion, properties.SwitchVector, "DOME_MOTION", ("DOME_CW", "DOME_CCW")),
    (dome.DomeTimer, properties.NumberVector, "DOME_TIMER", ("DOME_TIMER_VALUE",)),
    (dome.RelativeDomePosition, properties.NumberVector, "REL_DOME_POSITION", ("DOME_RELATIVE_POSITION",)),
    (dome.AbsoluteDomePosition, properties.NumberVector, "ABS_DOME_POSITION", ("DOME_ABSOLUTE_POSITION",)),
    (dome.DomeAbortMotion, properties.SwitchVector, "DOME_ABORT_MOTION", ("ABORT",)),
    (dome.DomeShutter, properties.SwitchVector, "DOME_SHUTTER", ("SHUTTER_OPEN", "SHUTTER_CLOSE")),
    (dome.DomeGoto, properties.SwitchVector, "DOME_GOTO", ("DOME_HOME", "DOME_PARK")),
    (dome.DomeParams, properties.NumberVector, "DOME_PARAMS", ("HOME_POSITION", "PARK_POSITION", "AUTOSYNC_THRESHOLD")),
    (
        dome.DomeAutosync,
        properties.SwitchVector,
        "DOME_AUTOSYNC",
        ("DOME_AUTOSYNC_ENABLE", "DOME_AUTOSYNC_DISABLE"),
    ),
    (
        dome.DomeMeasurements,
        properties.NumberVector,
        "DOME_MEASUREMENTS",
        ("DM_DOME_RADIUS", "DOME_SHUTTER_WIDTH", *_MEASUREMENT_TAIL),
    ),
    (
        dome.DomeMeasurementsIndi,
        properties.NumberVector,
        "DOME_MEASUREMENTS",
        ("DM_DOME_RADIUS", "DM_SHUTTER_WIDTH", *_MEASUREMENT_TAIL),
    ),
]

GUIDER_CASES = [
    (ccd.AbortExposure, "GUIDER_ABORT_EXPOSURE", ("ABORT",)),
    (ccd.Frame, "GUIDER_FRAME", ("X", "Y", "WIDTH", "HEIGHT")),
    (ccd.Temperature, "GUIDER_TEMPERATURE", ("GUIDER_TEMPERATURE_VALUE",)),
    (ccd.Cooler, "GUIDER_COOLER", ("COOLER_ON", "COOLER_OFF")),
    (ccd.CoolerPower, "GUIDER_COOLER_POWER", ("GUIDER_COOLER_VALUE",)),
    (ccd.FrameType, "GUIDER_FRAME_TYPE", ("FRAME_LIGHT", "FRAME_BIAS", "FRAME_DARK", "FRAME_FLAT")),
    (ccd.Binning, "GUIDER_BINNING", ("HOR_BIN", "VER_BIN")),
    (ccd.Compression, "GUIDER_COMPRESSION", ("INDI_ENABLED", "INDI_DISABLED")),
    (ccd.FrameReset, "GUIDER_FRAME_RESET", ("RESET",)),
    (ccd.Cfa, "GUIDER_CFA", ("CFA_OFFSET_X", "CFA_OFFSET_Y", "CFA_TYPE")),
]


def _member_names(vector):
    return tuple(element.name for element in vector.elements.values())


@pytest.mark.parametrize(
    ("factory", "vector_type", "name", "members"),
    CASES,
    ids=[factory.__name__ for factory, *_rest in CASES],
)
def test_standard_property_wire_names(factory, vector_type, name, members):
    vector = factory()
    assert isinstance(vector, vector_type)
    assert vector.name == name
    assert _member_names(vector) == members


@pytest.mark.parametrize(
    ("factory", "name", "members"),
    GUIDER_CASES,
    ids=[factory.__name__ for factory, *_rest in GUIDER_CASES],
)
def test_guider_property_names(factory, name, members):
    vector = factory(guider=True)
    assert vector.name == name
    assert _member_names(vector) == members


def test_guider_info_keeps_ccd_member_names():
    vector = ccd.Info(guider=True)
    assert vector.name == "GUIDER_INFO"
    assert _member_names(vector) == _INFO_MEMBERS


def test_guider_blob_is_ccd2():
    vector = ccd.Image(guider=True)
    assert isinstance(vector, properties.BLOBVector)
    assert vector.name == "CCD2"
    assert _member_names(vector) == ("CCD2",)


def test_abort_exposure_is_an_at_most_one_switch():
    vector = ccd.AbortExposure()
    assert isinstance(vector, properties.SwitchVector)
    assert vector.rule == const.SwitchRule.AT_MOST_ONE
    assert _member_names(vector) == ("ABORT",)


def test_active_devices_requires_a_known_member():
    with pytest.raises(ValueError, match="at least one"):
        common.ActiveDevices()
    with pytest.raises(ValueError, match="Unknown ACTIVE_DEVICES member"):
        common.ActiveDevices("ACTIVE_ROTATOR")


def test_active_devices_keeps_requested_members():
    vector = common.ActiveDevices("ACTIVE_CCD", "ACTIVE_TELESCOPE")
    assert isinstance(vector, properties.TextVector)
    assert vector.name == "ACTIVE_DEVICES"
    assert _member_names(vector) == ("ACTIVE_CCD", "ACTIVE_TELESCOPE")


def test_slew_rate_accepts_extra_switches():
    vector = telescope.TelescopeSlewRate(extra=("SLEW_CUSTOM",))
    assert _member_names(vector) == ("SLEW_GUIDE", "SLEW_CENTERING", "SLEW_FIND", "SLEW_MAX", "SLEW_CUSTOM")


def test_park_position_axes():
    assert _member_names(telescope.TelescopeParkPosition()) == ("PARK_RA", "PARK_DEC")
    assert _member_names(telescope.TelescopeParkPosition(system="horizontal")) == ("PARK_AZ", "PARK_ALT")


@pytest.mark.parametrize("factory", [telescope.TelescopeTrackRate, telescope.TelescopeTrackMode])
def test_track_mode_can_include_custom(factory):
    assert _member_names(factory()) == _TRACK_MODES
    assert _member_names(factory(custom=True)) == (*_TRACK_MODES, "TRACK_CUSTOM")


def test_filter_slot_minimum_defaults_to_one():
    element = next(iter(filterwheel.FilterSlot().elements.values()))
    assert element.min == 1


def test_read_only_defaults():
    assert telescope.TargetEodCoord().perm == const.Permissions.READ_ONLY
    assert ccd.CoolerPower().perm == const.Permissions.READ_ONLY
    assert ccd.Info().perm == const.Permissions.READ_ONLY
    assert ccd.Fps().perm == const.Permissions.READ_ONLY


def test_element_keys_do_not_hide_vector_attributes():
    compression = ccd.Compression()
    assert compression.enabled is True
    assert compression.enable.name == "INDI_ENABLED"
    assert compression.disable.name == "INDI_DISABLED"

    record_file = ccd.RecordFile()
    assert record_file.name == "RECORD_FILE"
    assert record_file.file_name.name == "RECORD_FILE_NAME"

    filter_name = filterwheel.FilterName()
    assert filter_name.name == "FILTER_NAME"
    assert filter_name.filter_name.name == "FILTER_NAME_VALUE"

    reverse = focuser.FocusReverseMotion()
    assert reverse.enabled is True
    assert reverse.enable.name == "ENABLED"
    assert reverse.disable.name == "DISABLED"

    indi_reverse = focuser.FocusReverseMotionIndi()
    assert indi_reverse.enable.name == "INDI_ENABLED"
    assert indi_reverse.disable.name == "INDI_DISABLED"


def test_perm_is_forwarded():
    port = common.DevicePort(
        label="Port",
        state=const.State.BUSY,
        perm=const.Permissions.READ_ONLY,
        timeout=5,
        enabled=False,
    )
    assert port.label == "Port"
    assert port.state == const.State.BUSY
    assert port.perm == const.Permissions.READ_ONLY
    assert port.timeout == 5
    assert port.enabled is False
    assert telescope.EquatorialCoord(perm=const.Permissions.READ_ONLY).perm == const.Permissions.READ_ONLY
    assert telescope.OnCoordSet(perm=const.Permissions.READ_ONLY).perm == const.Permissions.READ_ONLY
    assert ccd.Image(perm=const.Permissions.READ_ONLY).perm == const.Permissions.READ_ONLY
    assert ccd.Info(perm=const.Permissions.READ_WRITE).perm == const.Permissions.READ_WRITE
