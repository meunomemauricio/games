"""Interfaces for game Applications."""
from abc import ABC, abstractmethod
from typing import Optional

import pygame
from pygame.event import Event
from pygame.surface import Surface
from pygame.time import Clock

from games.utils import time_ms


def handle_quit(event: Event) -> None:
    """Handle the Quit events.

    :param event: PyGame Event object.
    """
    if event.type == pygame.QUIT:
        raise QuitApplication
    elif event.type == pygame.KEYUP and event.key == pygame.K_q:
        raise QuitApplication


class QuitApplication(Exception):
    """Quit the application if raised inside the Main Loop."""


class GameApplication(ABC):
    """Generic Game Application."""

    #: Applicaton Caption.
    CAPTION = None

    #: Max number of rendered frames that can be skipped. This is mostly
    #  relevant on slower machines, in case the time it takes to update the
    #  game state is greater than `TICK_STEP`.
    MAX_FRAMESKIP = 10

    #: Difference in time between ticks (ms)
    TICK_STEP = None

    def __init__(self):
        assert self.CAPTION, "Missing Application Caption."
        assert self.TICK_STEP, "Missing Tick Step."

        # Init PyGame
        pygame.init()
        pygame.display.set_caption(self.CAPTION)

        # Application Variables
        self._next_tick = time_ms()
        self._render_clock = Clock()
        self._running = True
        self._screen: Optional[Surface] = None

    # Interface

    @abstractmethod
    def _create_screen(self) -> Surface:
        """Create the Screen instance."""

    @abstractmethod
    def _handle_events(self, event: Event) -> None:
        """Handle game events.

        This method is is called for all events that happened since the last
        main loop iteration.

        :param event: Current event to be handled.
        """

    @abstractmethod
    def _handle_updates(self, tick: float) -> None:
        """Update game state.

        :param tick: Current tick in ms.
        """

    @abstractmethod
    def _draw_graphics(self, interp: float) -> None:
        """Draw contents of the frame to the Screen.

        :param interp: To allow smoother movement on screen, interpolation is
          used when rendering the screen between game state updates,
        """

    # Application Methods

    def _calc_interpolation(self) -> float:
        """Calculate the Interpolation between game ticks."""
        next_prediction = time_ms() + self.TICK_STEP - self._next_tick
        interp = next_prediction / self.TICK_STEP
        return max(min(interp, 1.0), 0.0)  # Clip between 0 and 1

    def _update_game_state(self, tick: float) -> None:
        """Update the game state."""
        for event in pygame.event.get():
            handle_quit(event=event)
            self._handle_events(event=event)

        self._handle_updates(tick=tick)

    def _render_graphics(self):
        """Render the frame and display it in the screen."""
        interpolation = self._calc_interpolation()
        self._draw_graphics(interp=interpolation)
        pygame.display.flip()
        self._render_clock.tick()

    def _main_loop(self):
        """Main Loop, repeated indefinitely, until it's stopped."""
        loops = 0
        current_tick = time_ms()
        while current_tick > self._next_tick and loops < self.MAX_FRAMESKIP:
            self._update_game_state(tick=current_tick)
            self._next_tick += self.TICK_STEP
            loops += 1

        self._render_graphics()

    def run(self) -> None:
        """Run the application."""
        self._screen = self._create_screen()
        while True:
            try:
                self._main_loop()
            except QuitApplication:
                break
