from typing import NewType

PermissionsType = NewType("PermissionsType", str)
StateType = NewType("StateType", str)
SwitchRuleType = NewType("SwitchRuleType", str)
SwitchStateType = NewType("SwitchStateType", str)
BLOBEnableType = NewType("BLOBEnableType", str)


class Permissions:
    READ_ONLY = PermissionsType("ro")
    WRITE_ONLY = PermissionsType("wo")
    READ_WRITE = PermissionsType("rw")


class State:
    IDLE = StateType("Idle")
    OK = StateType("Ok")
    BUSY = StateType("Busy")
    ALERT = StateType("Alert")


class SwitchRule:
    ONE_OF_MANY = SwitchRuleType("OneOfMany")
    AT_MOST_ONE = SwitchRuleType("AtMostOne")
    ANY_OF_MANY = SwitchRuleType("AnyOfMany")


class SwitchState:
    ON = SwitchStateType("On")
    OFF = SwitchStateType("Off")


class BLOBEnable:
    NEVER = BLOBEnableType("Never")
    ALSO = BLOBEnableType("Also")
    ONLY = BLOBEnableType("Only")
