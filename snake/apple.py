from functools import cached_property
from typing import Tuple

import pygame
from pygame.surface import Surface


class Apple:
    """Apple, Snake's favorite(?) food."""

    #: Apple Color
    COLOR = (0xFF, 0x00, 0x00)

    def __init__(self, x: int, y: int, grid_size: int):
        """Create a new Apple.

        :param x: Initial horizontal position, in grid coordinates.
        :param y: Initial vertical position, in grid coordinates.
        :param grid_size: Size of the Grid in Pixels.
        """
        self._x = x
        self._y = y
        self._grid_size = grid_size

    @property
    def render_pos(self) -> Tuple[int, int]:
        return self._x * self._grid_size, self._y * self._grid_size

    @cached_property
    def surface(self) -> Surface:
        """Apple Surface.

        Currently represented as a circle.
        """
        surface = Surface(size=(self._grid_size, self._grid_size))
        pygame.draw.circle(
            surface=surface,
            color=self.COLOR,
            center=(self._grid_size // 2, self._grid_size // 2),
            radius=self._grid_size // 2,
        )
        return surface
