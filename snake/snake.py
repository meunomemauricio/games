"""Represent the Main Protagonist."""
from enum import Enum
from typing import Mapping

import pygame
from pygame import Surface
from pygame.event import Event

from snake.grid import GridElement
from snake.utils import time_ms


class State(str, Enum):
    """Snake State."""

    STOPPED = "stopped"
    UP = "up"
    DOWN = "down"
    RIGHT = "right"
    LEFT = "left"


class Snake(GridElement):
    """🐍."""

    #: Colors
    HEAD_COLOR = (0x00, 0xFF, 0x00)

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
    SPEED = 500.0

    def __init__(self, step: int):
        """Create new Snake, controlled by the player.

        :param step: Size of the Grid in px.
        """
        super().__init__(x=0, y=0, step=step)

        self._state = State.STOPPED
        self._next_state = State.STOPPED  # State after handling input.

        # The moment from which it's possible to process movement again. Start
        # as the current time so it's executed right away.
        self._next_movement = time_ms()

    @property
    def surface(self) -> Surface:
        """Draw the snake on the surface."""
        surface = Surface(size=(self.size, self.size))
        surface.fill(color=self.HEAD_COLOR)
        return surface

    def handle_event(self, event: Event) -> None:
        """Handle events.

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

    def process_movement(self, tick: float) -> None:
        """Process the Snake movement.

        :param tick: Current tick in ms.
        """
        if tick < self._next_movement:
            return

        self._state = self._next_state
        if self._state == State.STOPPED:
            self._next_movement += self.SPEED
            return

        if self._state == State.UP:
            self.y -= 1
        elif self._state == State.DOWN:
            self.y += 1
        elif self._state == State.RIGHT:
            self.x += 1
        elif self._state == State.LEFT:
            self.x -= 1

        self._next_movement += self.SPEED
