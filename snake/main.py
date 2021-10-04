"""Main Application."""
from itertools import chain
from typing import Iterable

import pygame
from pygame.event import Event
from pygame.font import SysFont, get_default_font
from pygame.time import Clock

from snake.grid import Grid
from snake.settings import (
    BG_COLOR,
    CAPTION,
    DEBUG_COLOR,
    DEBUG_SIZE,
    SCREEN_SIZE,
    TICK_STEP,
)
from snake.ui import UserInterface
from snake.utils import Layer, multi_text, time_ms


class QuitApplication(Exception):
    """Quit the application if raised inside the Main Loop."""


def handle_quit(event: Event) -> None:
    """Handle the Quit events.

    :param event: PyGame Event object.
    """
    if event.type == pygame.QUIT:
        raise QuitApplication
    elif event.type == pygame.KEYUP and event.key == pygame.K_q:
        raise QuitApplication


class MainApp:
    """Main application."""

    def __init__(self, debug: bool):
        """Main Application.

        :param bp_name: Name of the Blueprint to be loaded.
        :param grid: If `True`, draw a grid on top of the screen.
        :param debug: If `True`, render the debug info on screen.
        """
        self._debug = debug

        # Init PyGame
        pygame.init()
        pygame.display.set_caption(CAPTION)

        # Application Variables
        self._next_tick = time_ms()
        self._render_clock = Clock()
        self._running = True

        self._screen = pygame.display.set_mode(
            size=SCREEN_SIZE,
            flags=pygame.SCALED,
        )

        # Game Elements
        self._fps_font = SysFont(get_default_font(), size=DEBUG_SIZE)
        self._grid = Grid()
        self._ui = UserInterface(grid=self._grid)

    @property
    def _debug_surface(self) -> Iterable[Layer]:
        """Debug text layers."""
        return multi_text(
            font=self._fps_font,
            color=DEBUG_COLOR,
            msgs=(
                f"FPS: {self._render_clock.get_fps()}",
                str(self._grid.snake),
                str(self._grid.apple),
            ),
        )

    def _handle_events(self):
        """Handle Game Events."""
        for event in pygame.event.get():
            handle_quit(event=event)
            self._grid.handle_event(event=event)

    def _render_graphics(self) -> None:
        """Render the frame and display it in the screen."""
        self._screen.fill(color=BG_COLOR)
        layer_groups = [self._grid.layers, self._ui.layers]
        if self._debug:
            layer_groups.append(self._debug_surface)

        self._screen.blits(chain(*layer_groups))
        pygame.display.flip()
        self._render_clock.tick()

    def _main_loop(self) -> None:
        """Main Application Loop."""
        if time_ms() > self._next_tick:
            self._grid.update_state()
            self._next_tick += TICK_STEP

        self._handle_events()
        self._render_graphics()

    def run(self) -> None:
        """Run the application."""
        while True:
            try:
                self._main_loop()
            except QuitApplication:
                break
