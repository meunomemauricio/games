"""Declare auxiliary functions."""

import time
from typing import Iterable, Tuple

from pygame.color import Color
from pygame.font import Font
from pygame.surface import Surface

SizeTuple = Tuple[int, int]
Layer = Tuple[Surface, SizeTuple]

Point = "snake.elements.Point"

PINK = Color(0xFF, 0x00, 0xFF)


def point_collision(point_a: Point, point_b: Point) -> bool:
    """Detect collision between two points."""
    return point_a.x == point_b.x and point_a.y == point_b.y


def multi_text(
    font: Font, color: Color, msgs: Iterable[str]
) -> Iterable[Layer]:
    """Convert a list of messages into Layers to be blitted to the screen."""
    total_y = sum(font.size(msg)[1] for msg in msgs)  # Sum of vertical size
    surfaces = [font.render(msg, True, color) for msg in msgs]
    positions = [(0, y) for y in range(0, total_y, font.get_height())]
    return zip(surfaces, positions)


def time_ms() -> float:
    """Return current time in milliseconds."""
    return time.time() * 1000
