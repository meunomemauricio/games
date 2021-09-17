"""Define base game elements."""
from random import randint
from typing import Optional, Tuple

from pygame.color import Color
from pygame.rect import Rect

from snake.utils import PINK

Grid = "snake.grid.Grid"


class GridElement:
    """An element that fits into a Grid unit."""

    def __init__(
        self,
        grid: "Grid",
        x: Optional[int] = None,
        y: Optional[int] = None,
        color: Color = None,
    ):
        """Create new Grid Element.

        :param x: Initial horizontal position, in grid coordinates.
        :param y: Initial vertical position, in grid coordinates.
        :param grid: Grid object.
        """
        self._grid = grid
        self.x = x if x is not None else randint(0, self._grid.size[0] - 1)
        self.y = y if y is not None else randint(0, self._grid.size[1] - 1)
        self.color = color if color is not None else PINK

    @property
    def rect(self) -> Rect:
        """Rectangle representing the element."""
        return Rect(
            self.x * self._grid.step,
            self.y * self._grid.step,
            self._grid.step,
            self._grid.step,
        )

    @property
    def render_pos(self) -> Tuple[int, int]:
        """Render position in screen coordinates."""
        return self.x * self._grid.step, self.y * self._grid.step
