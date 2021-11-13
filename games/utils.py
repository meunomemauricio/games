"""Declare auxiliary functions."""

import time
from typing import Iterable, NamedTuple, Tuple

from pygame.color import Color
from pygame.font import Font
from pygame.surface import Surface

SizeTuple = Tuple[int, int]

Point = "snake.elements.Point"

PINK = Color(0xFF, 0x00, 0xFF)


class Position(NamedTuple):
    """Render position (screen coordinates)."""

    x: int
    y: int


class Layer(NamedTuple):
    """A Surface Layer."""

    surface: Surface
    pos: Position

    def __add__(self, offset: Position):
        if isinstance(offset, Position):
            raise ValueError("Offset needs to be an integer.")

        self.pos = Position(self.pos.y + offset.y, self.pos.y + offset.y)


def multi_text(
    font: Font, color: Color, msgs: Iterable[str]
) -> Iterable[Layer]:
    """Convert a list of messages into Layers to be blitted to the screen."""
    total_y = sum(font.size(msg)[1] for msg in msgs)  # Sum of vertical size
    surfaces = [font.render(msg, True, color) for msg in msgs]
    positions = [Position(0, y) for y in range(0, total_y, font.get_height())]
    return (Layer(s, p) for s, p in zip(surfaces, positions))


def time_ms() -> float:
    """Return current time in milliseconds."""
    return time.time() * 1000
