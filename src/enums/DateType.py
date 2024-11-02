from enum import IntEnum, auto


class DateType(IntEnum):
    DAILY: int = auto()
    MONTHLY: int = auto()
    YEARLY: int = auto()
