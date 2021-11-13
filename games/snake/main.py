"""Main Application."""
from itertools import chain
from typing import Iterable

import pygame
from pygame.event import Event
from pygame.font import SysFont, get_default_font
from pygame.surface import Surface

from games.application import GameApplication
from games.snake.grid import Grid
from games.snake.settings import (
    BG_COLOR,
    CAPTION,
    DEBUG_COLOR,
    DEBUG_SIZE,
    SCREEN_SIZE,
    TICK_STEP,
)
from games.snake.ui import UserInterface
from games.utils import Layer, multi_text


class MainApp(GameApplication):
    """Main application."""

    CAPTION = CAPTION
    TICK_STEP = TICK_STEP

    def __init__(self, debug: bool):
        """Main Application.

        :param bp_name: Name of the Blueprint to be loaded.
        :param grid: If `True`, draw a grid on top of the screen.
        :param debug: If `True`, render the debug info on screen.
        """
        super().__init__()

        self._debug = debug

        # Game Elements
        self._fps_font = SysFont(get_default_font(), size=DEBUG_SIZE)
        self._grid = Grid()
        self._ui = UserInterface(grid=self._grid)

    @property
    def _debug_layers(self) -> Iterable[Layer]:
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

    def _create_screen(self) -> Surface:
        return pygame.display.set_mode(
            size=SCREEN_SIZE,
            flags=pygame.SCALED,
        )

    def _handle_events(self, event: Event) -> None:
        """Handle Game Events."""
        self._grid.handle_event(event=event)

    def _handle_updates(self, tick: float) -> None:
        self._grid.update_state()

    def _draw_graphics(self, interp: float) -> None:
        """Render the frame and display it in the screen."""
        layer_groups = [self._grid.layers, self._ui.layers]
        if self._debug:
            layer_groups.append(self._debug_layers)

        self._screen.fill(color=BG_COLOR)
        self._screen.blits(chain(*layer_groups))
        pygame.display.flip()
        self._render_clock.tick()
