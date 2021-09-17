"""Define base game elements."""
from abc import ABC, abstractmethod
from random import randint
from typing import Optional, Tuple

from pygame.color import Color
from pygame.rect import Rect
from pygame.surface import Surface

from snake.utils import PINK, Layer

Grid = "snake.grid.Grid"


class GridElement(ABC):
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
        # Use pink to highlight default case.
        self.color = color if color is not None else PINK

    @property
    def layer(self) -> Layer:
        """Rendering Layer."""
        return self.surface, self.render_pos

    @property
    @abstractmethod
    def surface(self) -> Surface:
        """Element Surface.

        Needs to fit into a grid cell.
        """

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
