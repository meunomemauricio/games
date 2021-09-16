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
    for msg in msgs:
        font.render(msg, True, color)
