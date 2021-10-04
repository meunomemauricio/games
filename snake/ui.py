"""User Interface."""
from typing import Iterable

from pygame.surface import Surface

from snake.grid import Grid
from snake.settings import SCREEN_WIDTH, UI_HEIGHT
from snake.utils import Layer, Position


class UserInterface:
    """User Interface."""

    def __init__(self, grid: Grid):
        """Instantiate User Interface.

        :param grid: Game Grid.
        """
        self._grid = grid

    @property
    def layers(self) -> Iterable[Layer]:
        """Rendering Layers."""
        surface = Surface(size=(SCREEN_WIDTH, UI_HEIGHT))
        return (Layer(surface, Position(0, 0)),)
