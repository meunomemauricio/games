"""Snake's favorite(?) food."""
from functools import cached_property

import pygame
from pygame.color import Color
from pygame.surface import Surface

from snake.elements import GridElement, RandomPoint


class Apple(GridElement):
    """Apple."""

    #: Apple Color
    COLOR = Color(0xFF, 0x00, 0x00)

    def __str__(self) -> str:
        return f"Apple: p={self.p}"

    @cached_property
    def surface(self) -> Surface:
        """Apple Surface.

        Currently represented as a circle.
        """
        surface = Surface(size=(self._grid.step, self._grid.step))
        pygame.draw.circle(
            surface=surface,
            color=self.COLOR,
            center=(self._grid.step // 2, self._grid.step // 2),
            radius=self._grid.step // 2,
        )
        return surface

    def respawn(self) -> None:
        """Shuffle the Apple position."""
        self.p = RandomPoint(grid=self._grid)
