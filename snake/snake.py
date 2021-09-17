"""Represent the Main Protagonist."""
from enum import Enum
from functools import cached_property
from typing import List, Mapping

import pygame
from pygame import Surface
from pygame.event import Event

from snake.apple import Apple
from snake.elements import GridElement

Grid = "snake.grid.Grid"


class State(str, Enum):
    """Snake State."""

    STOPPED = "S"
    UP = "U"
    DOWN = "D"
    RIGHT = "R"
    LEFT = "L"


class Collision(str, Enum):
    """Collision State."""

    NONE = "N"
    APPLE = "A"
    BODY = "B"
    SCREEN = "S"


class Segment(GridElement):
    """Snake Body Segment."""

    COLOR = (0x00, 0xBB, 0x00)

    @cached_property
    def surface(self) -> Surface:
        """Draw the Segment Surface."""
        surface = Surface(size=(self._grid.step, self._grid.step))
        surface.fill(color=self.COLOR)
        return surface


class Snake(Segment):
    """🐍."""

    COLOR = (0x00, 0xFF, 0x00)

    #: Convert a pygame event into a Snake State.
    STATE_MAP: Mapping[Event, State] = {
        pygame.K_UP: State.UP,
        pygame.K_DOWN: State.DOWN,
        pygame.K_RIGHT: State.RIGHT,
        pygame.K_LEFT: State.LEFT,
    }

    #: Prevent the snake from reversing on itself.
    FORBIDDEN_MOVEMENT: Mapping[State, Event] = {
        State.UP: pygame.K_DOWN,
        State.DOWN: pygame.K_UP,
        State.RIGHT: pygame.K_LEFT,
        State.LEFT: pygame.K_RIGHT,
    }

    #: Snake Speed, defined as how long it takes to move a grid unit (in ms).
    SPEED = 200.0

    def __init__(self, grid: Grid, apple: Apple):
        """Create new Snake, controlled by the player.

        :param grid: Object representing the grid.
        """
        super().__init__(grid=grid)

        self._apple = apple

        self._state = State.STOPPED
        self._next_state = State.STOPPED  # State after handling input.

        self._last_collision = Collision.NONE

        self.body: List[Segment] = []

    def __len__(self) -> int:
        """Snake Length, in number of segments, including the head."""
        return len(self.body) + 1

    def __str__(self) -> str:
        """Debug information."""
        return f"Snake: x={self.x} y={self.y} B={len(self)}"

    def handle_event(self, event: Event) -> None:
        """Handle Game Events.

        :param event: Pygame Event to be handled.
        """
        if event.type != pygame.KEYDOWN:
            return

        forbidden = self.FORBIDDEN_MOVEMENT.get(self._state)
        if event.key == forbidden:
            return

        next_state = self.STATE_MAP.get(event.key)
        if next_state:
            self._next_state = next_state

    def _process_movement(self) -> None:
        """Process the Snake movement."""
        if self._state == State.UP:
            self.y -= 1
        elif self._state == State.DOWN:
            self.y += 1
        elif self._state == State.RIGHT:
            self.x += 1
        elif self._state == State.LEFT:
            self.x -= 1

    def _process_collision(self) -> None:
        """Detect Collision between Snake and other game elements."""
        if self.x == self._apple.x and self.y == self._apple.y:
            self._apple.shuffle_position()
            self._last_collision = Collision.APPLE
            return

    def update_state(self) -> None:
        """Update the Snake state."""
        self._state = self._next_state
        if self._state == State.STOPPED:
            return

        if self._last_collision == Collision.APPLE:
            self.body.append(Segment(grid=self._grid, x=self.x, y=self.y))
            self._last_collision = Collision.NONE

        self._process_movement()
        self._process_collision()
