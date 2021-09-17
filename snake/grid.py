"""Define the grid and its generic elements."""
from functools import cached_property
from typing import Tuple

import pygame
from pygame.surface import Surface

from snake.apple import Apple
from snake.snake import Snake


class Grid:
    """Game Grid."""

    def __init__(
        self,
        size: Tuple[int, int],
        step: int,
        alpha: int,
        color: Tuple[int, int, int],
        line: int,
    ):
        """Create a new Grid.

        :param step: Step size in px (square cells).
        :param size: Grid Size, the total number of cells in each coordinate.
        :param alpha: Grid alpha.
        :param color: Grid color.
        :param line: Line Width in px.
        """
        self.step = step
        self.size = size

        self.alpha = alpha
        self.color = color
        self.line = line

        self.resolution = size[0] * step, size[1] * step
        self.width, self.height = self.resolution

        self.apple = Apple(grid=self)
        self.snake = Snake(grid=self, apple=self.apple)

    @cached_property
    def base_surface(self) -> Surface:
        """Base surface representing the Grid."""
        surface = Surface(size=self.resolution, flags=pygame.SRCALPHA)
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

    @property
    def surface(self) -> Surface:
        """Grid with other game elements rendered."""
        surface = Surface(size=self.resolution, flags=pygame.SRCALPHA)
        layers = [
            (self.base_surface, (0, 0)),
            (self.apple.surface, self.apple.render_pos),
            (self.snake.surface, self.snake.render_pos),
        ]
        # layers.extend((b.surface, b.render_pos) for b in self.snake.body)
        surface.blits(layers)
        return surface
