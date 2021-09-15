"""Represent the Main Protagonist."""
from enum import Enum
from typing import Mapping, Tuple

import pygame
from pygame import Surface
from pygame.event import Event

from snake.utils import time_ms


class Direction(str, Enum):
    """Snake Direction."""

    UP = "up"
    DOWN = "down"
    RIGHT = "right"
    LEFT = "left"


class Snake:
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

    def __init__(self, grid_size: int):
        """Create new Snake, controlled by the player.

        :param grid_size: Size of the Grid in Pixels.
        """
        self._grid_size = grid_size

        self._x: int = 0
        self._y: int = 0

        self._direction = Direction.RIGHT

        # Used to control the snake speed
        self._next_movement: float = time_ms()

    @property
    def render_pos(self) -> Tuple[int, int]:
        return self._x * self._grid_size, self._y * self._grid_size

    @property
    def surface(self) -> Surface:
        """Draw the snake on the surface."""
        surface = Surface(size=(self._grid_size, self._grid_size))
        surface.fill(color=self.HEAD_COLOR)
        return surface

    def handle_event(self, event: Event) -> None:
        """Handle events."""
        if event.type == pygame.KEYDOWN:
            new_direction = self.DIRECTION_MAP.get(event.key)
            if new_direction:
                self._direction = new_direction

    def process_movement(self, tick: float) -> None:
        """Process the Snake movement.

        :param tick: Current tick in ms.
        """
        if tick < self._next_movement:
            return

        if self._direction == Direction.UP:
            self._y -= 1
        elif self._direction == Direction.DOWN:
            self._y += 1
        elif self._direction == Direction.RIGHT:
            self._x += 1
        elif self._direction == Direction.LEFT:
            self._x -= 1

        self._next_movement += self.SPEED
