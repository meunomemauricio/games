"""Define the grid and its generic elements."""
from functools import cached_property
from itertools import chain
from typing import Iterable

import pygame
from pygame.event import Event
from pygame.rect import Rect
from pygame.surface import Surface

from games.snake.apple import Apple
from games.snake.settings import (
    GRID_ALPHA,
    GRID_COLOR,
    GRID_LINE,
    GRID_SIZE,
    GRID_STEP,
    UI_HEIGHT,
)
from games.snake.snake import Snake
from games.utils import Layer, Position


class Grid:
    """Game Grid."""

    def __init__(self):
        """Create a new Grid."""
        self.resolution = GRID_SIZE[0] * GRID_STEP, GRID_SIZE[1] * GRID_STEP
        self.width, self.height = self.resolution
        self.rect = Rect((0, UI_HEIGHT), self.resolution)

        self.apple = Apple(grid=self)
        self.snake = Snake(grid=self)

        self._surface = Surface(size=self.resolution)

    @cached_property
    def base_surface(self) -> Surface:
        """Base surface representing the Grid."""
        surface = Surface(size=self.resolution, flags=pygame.SRCALPHA)
        surface.set_alpha(GRID_ALPHA)
        for x in range(0, self.width, GRID_STEP):
            for y in range(0, self.height, GRID_STEP):
                pygame.draw.rect(
                    surface=surface,
                    color=GRID_COLOR,
                    rect=pygame.Rect((x, y), (GRID_STEP, GRID_STEP)),
                    width=GRID_LINE,
                )

        return surface

    @property
    def layers(self) -> Iterable[Layer]:
        """Surface layers to be blitted to the screen."""
        layers = (
            Layer(self.base_surface, Position(0, UI_HEIGHT)),
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
