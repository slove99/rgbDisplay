from enum import IntEnum

class Operation(IntEnum):
    OFF = 0
    MIX = 1
    CLOCK = 2
    MUSIC = 3
    NEWS = 4

class Dimensions(IntEnum):
    DISPLAY_HEIGHT = 16
    DISPLAY_WIDTH = 32
    DISPLAY_CHAIN_LEN = 2
