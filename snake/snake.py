"""Represent the Main Protagonist."""
from enum import Enum
from typing import Mapping

import pygame
from pygame import Surface
from pygame.event import Event

from snake.grid import GridElement


class Direction(str, Enum):
    """Snake Direction."""

    UP = "up"
    DOWN = "down"
    RIGHT = "right"
    LEFT = "left"


class Snake(GridElement):
    """Snake."""

    #: Colors
    HEAD_COLOR = (0x00, 0xFF, 0x00)

    #: Convert a pygame event into a Snake Direction.
    DIRECTION_MAP: Mapping[Event, Direction] = {
        pygame.K_UP: Direction.UP,
        pygame.K_DOWN: Direction.DOWN,
        pygame.K_RIGHT: Direction.RIGHT,
        pygame.K_LEFT: Direction.LEFT,
    }

    #: Snake Speed, defined as how long it takes to move a grid unit (in ms).
    SPEED = 500.0

    def __init__(self, step: int):
        """Create new Snake, controlled by the player.

        :param step: Size of the Grid in px.
        """
        super().__init__(x=0, y=0, step=step)

        self._direction = Direction.RIGHT

    @property
    def surface(self) -> Surface:
        """Draw the snake on the surface."""
        surface = Surface(size=(self.size, self.size))
        surface.fill(color=self.HEAD_COLOR)
        return surface

    def handle_event(self, event: Event) -> None:
        """Handle events."""
        if event.type == pygame.KEYDOWN:
            new_direction = self.DIRECTION_MAP.get(event.key)
            if new_direction:
                self._direction = new_direction

    def process_movement(self) -> None:
        """Process the Snake movement."""
        if self._direction == Direction.UP:
            self.y -= 1
        elif self._direction == Direction.DOWN:
            self.y += 1
        elif self._direction == Direction.RIGHT:
            self.x += 1
        elif self._direction == Direction.LEFT:
            self.x -= 1
