"""Declare auxiliary functions."""

import time
from typing import Iterable, Tuple

from pygame.font import Font
from pygame.surface import Surface


def time_ms() -> float:
    """Return current time in milliseconds."""
    return time.time() * 1000


def multi_text(
    font: Font, color: Tuple[int, int, int], msgs: Iterable[str]
) -> Surface:
    """Generate a surface from multiple text messages."""
    surface_x = max(font.size(msg)[0] for msg in msgs)
    surface_y = sum(font.size(msg)[1] for msg in msgs)
    surfaces = [font.render(msg, True, color) for msg in msgs]
    positions = [(0, y) for y in range(0, surface_y, font.get_height())]
    surface = Surface(size=(surface_x, surface_y))
    surface.blits(zip(surfaces, positions))
    return surface
