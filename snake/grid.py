"""Define the grid and its generic elements."""
from functools import cached_property
from itertools import chain
from typing import Iterable

import pygame
from pygame.color import Color
from pygame.event import Event
from pygame.rect import Rect
from pygame.surface import Surface

from snake.apple import Apple
from snake.snake import Snake
from snake.utils import Layer, Position, SizeTuple


class Grid:
    """Game Grid."""

    def __init__(
        self,
        size: SizeTuple,
        step: int,
        alpha: int,
        color: Color,
        line: int,
        offset: int,
    ):
        """Create a new Grid.

        :param size: Grid Size, the total number of cells in each coordinate.
        :param step: Step size in px (square cells).
        :param alpha: Grid alpha.
        :param color: Grid color.
        :param line: Line Width in px.
        :param offset: Height offset (UI height).
        """
        self.size = size
        self.step = step

        self.alpha = alpha
        self.color = color
        self.line = line

        self.offset = offset

        self.resolution = size[0] * step, size[1] * step
        self.width, self.height = self.resolution
        self.rect = Rect((0, offset), self.resolution)

        self.apple = Apple(grid=self)
        self.snake = Snake(grid=self)

        self._surface = Surface(size=self.resolution)

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
    def layers(self) -> Iterable[Layer]:
        """Surface layers to be blitted to the screen."""
        layers = (
            Layer(self.base_surface, Position(0, self.offset)),
            self.apple.layer,
        )
        return chain(layers, self.snake.layers)

    def handle_event(self, event: Event) -> None:
        """Handle Game Events.

        :param event: Pygame Event to be handled.
        """
        self.snake.handle_event(event=event)

    def update_state(self) -> None:
        """Update Grid State."""
        self.snake.update_state()
