"""Represent the Main Protagonist."""
from collections import deque
from enum import Enum
from functools import cached_property
from typing import Mapping

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


class Segment(GridElement):
    """Snake Body Segment."""

    COLOR = (0x00, 0xBB, 0x00)

    @cached_property
    def surface(self) -> Surface:
        """Draw the Segment Surface."""
        surface = Surface(size=(self._grid.step, self._grid.step))
        surface.fill(color=self.COLOR)
        return surface


class Snake:
    """🐍."""

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
        :param apple: Apple object.
        """
        self._grid = grid
        self._apple = apple

        self._state = State.STOPPED
        self._next_state = State.STOPPED  # State after handling input.

        #: Snake Body, represented as a Deque.
        #:
        #: The leftmost (body[0]) element is the head and the last element is
        #: the tail.
        #:
        #: For every step (without collision), a new head is created in the
        #: next grid cell (position based on next state) and the tail segment
        #: is removed. If it collides with the apple, the tail is kept, giving
        #: the impression that the snake has grown. Each in-between segment is
        #: kept in place, preserving its shape.
        self.body: deque[Segment] = deque([Segment(grid=grid)])

    def __len__(self) -> int:
        """Number of segments."""
        return len(self.body)

    def __str__(self) -> str:
        """Debug information."""
        return f"Snake: x={self.body[0].x} y={self.body[0].y} B={len(self)}"

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
        """Process the Snake movement.

        Create new head, based on the current state.
        """
        new_x = self.body[0].x
        new_y = self.body[0].y
        if self._state == State.UP:
            new_y -= 1
        elif self._state == State.DOWN:
            new_y += 1
        elif self._state == State.RIGHT:
            new_x += 1
        elif self._state == State.LEFT:
            new_x -= 1

        new_head = Segment(grid=self._grid, x=new_x, y=new_y)
        self.body.appendleft(new_head)

    def _process_collision(self) -> None:
        """Detect Collision between Snake and other game elements."""
        if self.body[0].x == self._apple.x and self.body[0].y == self._apple.y:
            self._apple.respawn()
            return  # Skip the pop, so we'll grow

        # Remove the last segment of the snake after each movement, as the
        # default case, since the movement added a new segment.
        self.body.pop()

    def update_state(self) -> None:
        """Update the Snake state."""
        self._state = self._next_state
        if self._state == State.STOPPED:
            return

        self._process_movement()
        self._process_collision()
