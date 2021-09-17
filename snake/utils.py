"""Declare auxiliary functions."""

import time
from typing import Iterable, Tuple

from pygame.color import Color
from pygame.font import Font
from pygame.surface import Surface

Layer = Tuple[Surface, Tuple[int, int]]

PINK = Color(0xFF, 0x00, 0xFF)


def time_ms() -> float:
    """Return current time in milliseconds."""
    return time.time() * 1000


def multi_text(
    font: Font, color: Tuple[int, int, int], msgs: Iterable[str]
) -> Iterable[Layer]:
    """Generate a surface from multiple text messages."""
    total_y = sum(font.size(msg)[1] for msg in msgs)
    surfaces = [font.render(msg, True, color) for msg in msgs]
    positions = [(0, y) for y in range(0, total_y, font.get_height())]
    return zip(surfaces, positions)
