"""Game Enums."""
from enum import Enum


class State(str, Enum):
    """Snake State."""

    DEAD = "X"
    STOPPED = "S"

    UP = "U"
    DOWN = "D"
    RIGHT = "R"
    LEFT = "L"
