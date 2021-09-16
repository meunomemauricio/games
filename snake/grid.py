"""Define the grid and its generic elements."""
import random
from functools import cached_property
from typing import Tuple

import pygame
from pygame.rect import Rect
from pygame.surface import Surface


class Grid:
    """Game Grid."""

    def __init__(
        self,
        width: int,
        height: int,
        alpha: int,
        color: Tuple[int, int, int],
        line: int,
        step: int,
    ):
        """Create a new Grid.

        :param width: Total grid width.
        :param height: Total grid height.
        :param alpha: Grid alpha.
        :param color: Grid color.
        :param line: Line Width in px.
        :param step: Step size in px (assumed square).
        """
        self.width = width
        self.height = height
        self.alpha = alpha
        self.color = color
        self.line = line
        self.step = step

    @cached_property
    def surface(self) -> Surface:
        """A surface representing the Grid."""
        surface = Surface(
            size=(self.width, self.height), flags=pygame.SRCALPHA
        )
        surface.set_alpha(self.alpha)
        for x in range(0, self.width, self.step):
            for y in range(0, self.height, self.step):
                pygame.draw.rect(
                    surface=surface,
                    color=self.color,
                    rect=pygame.Rect((x, y), (self.step, self.step)),
                    width=self.line,
                )

        return surface


class GridElement:
    """An element that fit into a Grid unit."""

    def __init__(self, grid: Grid):
        """Create new Grid Element.

        :param x: Initial horizontal position, in grid coordinates.
        :param y: Initial vertical position, in grid coordinates.
        :param grid: Grid object.
        """
        self._grid = grid

        self.x = random.randint(1, 10)
        self.y = random.randint(1, 10)

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
