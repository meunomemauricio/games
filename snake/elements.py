"""Define base game elements."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import randint
from typing import Optional, Tuple

from pygame.color import Color
from pygame.rect import Rect
from pygame.surface import Surface

from snake.experimental.enums import State
from snake.utils import PINK, Layer

Grid = "snake.grid.Grid"


@dataclass
class Point:
    """A Point in the Grid."""

    x: int
    y: int

    def clone(self, state: State) -> "Point":
        """Return a new point in a location based on the State."""
        new_x, new_y = self.x, self.y
        if state == State.UP:
            new_y -= 1
        elif state == State.DOWN:
            new_y += 1
        elif state == State.RIGHT:
            new_x += 1
        elif state == State.LEFT:
            new_x -= 1

        return Point(x=new_x, y=new_y)


class RandomPoint(Point):
    """A random point in the grid."""

    def __init__(self, grid: Grid):
        x = randint(0, grid.size[0] - 1)
        y = randint(0, grid.size[1] - 1)
        super().__init__(x=x, y=y)


class GridElement(ABC):
    """An element that fits into a Grid unit."""

    def __init__(
        self,
        grid: Grid,
        point: Optional[Point] = None,
        color: Color = None,
    ):
        """Create new Grid Element.

        :param x: Initial horizontal position, in grid coordinates.
        :param y: Initial vertical position, in grid coordinates.
        :param grid: Grid object.
        """
        self._grid = grid
        self.p: Point = point or RandomPoint(grid=grid)

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
            self.p.x * self._grid.step,
            self.p.y * self._grid.step,
            self._grid.step,
            self._grid.step,
        )

    @property
    def render_pos(self) -> Tuple[int, int]:
        """Render position in screen coordinates."""
        return self.p.x * self._grid.step, self.p.y * self._grid.step
