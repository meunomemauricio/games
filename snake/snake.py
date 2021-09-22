"""Represent the Main Protagonist."""
from collections import deque
from functools import cached_property
from typing import Mapping

import pygame
from pygame import Surface
from pygame.event import Event

from snake.elements import GridElement
from snake.experimental.enums import State

Grid = "snake.grid.Grid"


class Segment(GridElement):
    """Snake Body Segment."""

    COLOR = (0x00, 0xBB, 0x00)

    @cached_property
    def surface(self) -> Surface:
        """Draw the Segment Surface."""
        surface = Surface(size=(self._grid.step, self._grid.step))
        surface.fill(color=self.COLOR)
        return surface


class KillSnake(Exception):
    """Raised if the Snake eats itself or go off screen."""


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

    def __init__(self, grid: Grid):
        """Create new Snake, controlled by the player.

        :param grid: Object representing the grid.
        :param apple: Apple object.
        """
        self._grid = grid
        self._apple = grid.apple

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
        head = self.body[0]
        return (
            f"Snake: x={head.p.x} y={head.p.y} B={len(self)} S={self._state}"
        )

    def _body_collision(self) -> bool:
        """Detect collision between the head and the rest of the body."""
        head = self.body[0].p
        body_segments = iter(self.body)
        next(body_segments)  # Skip the Head
        for segment in body_segments:
            if head.collision(segment.p):
                return True

        return False

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
        new_point = self.body[0].p.clone(state=self._state)
        new_head = Segment(grid=self._grid, point=new_point)
        self.body.appendleft(new_head)

    def _process_collision(self) -> None:
        """Detect Collision between Snake and other game elements."""
        head = self.body[0]
        if self._body_collision():
            self._next_state = State.DEAD
            raise KillSnake

        if not head.rect.colliderect(self._grid.rect):
            raise KillSnake

        if head.p.collision(self._apple.p):
            self._apple.respawn()
            return  # Skip the pop, so it'll grow.

        # Remove tail after each movement to preserve its length.
        self.body.pop()

    def update_state(self) -> None:
        """Update the Snake state."""
        if self._state == State.DEAD:
            return

        self._state = self._next_state
        if self._state == State.STOPPED:
            return

        self._process_movement()
        try:
            self._process_collision()
        except KillSnake:
            self._state = State.DEAD
