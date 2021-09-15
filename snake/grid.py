"""Define the grid and its generic elements."""
from typing import Tuple

from pygame.rect import Rect


class GridElement:
    """An element that fit into a Grid unit."""

    def __init__(self, x: int, y: int, size: int):
        """Create new Grid Element.

        :param x: Initial horizontal position, in grid coordinates.
        :param y: Initial vertical position, in grid coordinates.
        :param size: Size of the Grid in Pixels.
        """
        self.x = x
        self.y = y
        self.size = size

    @property
    def rect(self) -> Rect:
        """Rectangle representing the element."""
        return Rect(
            self.x * self.size, self.y * self.size, self.size, self.size
        )

    @property
    def render_pos(self) -> Tuple[int, int]:
        """Render position in screen coordinates."""
        return self.x * self.size, self.y * self.size
