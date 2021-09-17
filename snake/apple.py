"""Snake's favorite(?) food."""
import random
from functools import cached_property

import pygame
from pygame.surface import Surface

from snake.elements import GridElement


class Apple(GridElement):
    """Apple"""

    #: Apple Color
    COLOR = (0xFF, 0x00, 0x00)

    def __str__(self) -> str:
        return f"Apple: x={self.x} y={self.y}"

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

    def shuffle_position(self) -> None:
        """Shuffle the Apple position."""
        self.x = random.randint(0, self._grid.size[0] - 1)
        self.y = random.randint(0, self._grid.size[1] - 1)
