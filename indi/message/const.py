class Permissions:
    READ_ONLY = "ro"
    WRITE_ONLY = "wo"
    READ_WRITE = "rw"


class State:
    IDLE = "Idle"
    OK = "Ok"
    BUSY = "Busy"
    ALERT = "Alert"


class SwitchRule:
    ONE_OF_MANY = "OneOfMany"
    AT_MOST_ONE = "AtMostOne"
    ANY_OF_MANY = "AnyOfMany"


class SwitchState:
    ON = "On"
    OFF = "Off"


class BLOBEnable:
    NEVER = "Never"
    ALSO = "Also"
    ONLY = "Only"
