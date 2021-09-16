"""Main Application."""

import pygame
from pygame.event import Event
from pygame.font import SysFont, get_default_font
from pygame.surface import Surface
from pygame.time import Clock

from snake.apple import Apple
from snake.grid import Grid
from snake.snake import Snake
from snake.utils import time_ms


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

    #: Screen/Window parameters.
    CAPTION = "Snake v0.1"

    WIDTH = 800
    HEIGHT = 800

    BG_COLOR = (0x00, 0x00, 0x00)

    #: FPS meter parameters.
    FPS_SIZE = 25
    FPS_COLOR = (0xFF, 0x00, 0x00)

    #: Grid parameters.
    GRID_ALPHA = 50
    GRID_COLOR = (0xFF, 0xFF, 0xFF)
    GRID_LINE = 1
    GRID_SIZE = (20, 20)
    GRID_STEP = 80

    #: Difference in time between ticks.
    TICK_STEP = 10.0  # ms

    #: Max number of rendered frames that can be skipped. This is mostly
    #  relevant on slower machines, in case the time it takes to update the
    #  game state is greater than `TICK_STEP`.

    MAX_FRAMESKIP = 10

    def __init__(self, debug: bool):
        """Main Application.

        :param bp_name: Name of the Blueprint to be loaded.
        :param grid: If `True`, draw a grid on top of the screen.
        :param debug: If `True`, render the debug info on screen.
        """
        self._debug = debug

        # Init PyGame
        pygame.init()
        pygame.display.set_caption(self.CAPTION)

        # Application Variables
        self._next_tick = time_ms()
        self._render_clock = Clock()
        self._running = True

        # Game Elements
        self._fps_font = SysFont(get_default_font(), self.FPS_SIZE)
        self._grid = Grid(
            size=self.GRID_SIZE,
            step=self.GRID_STEP,
            alpha=self.GRID_ALPHA,
            color=self.GRID_COLOR,
            line=self.GRID_LINE,
        )
        self._screen = pygame.display.set_mode(size=self._grid.resolution)
        self._snake = Snake(grid=self._grid)
        self._apple = Apple(grid=self._grid)

    @property
    def _debug_surface(self) -> Surface:
        """FPS Meter Surface."""
        msg = (
            f"FPS: {self._render_clock.get_fps()}",
            f"Snake: x={self._snake.x} y={self._snake.y}",
        )
        return self._fps_font.render(" | ".join(msg), True, self.FPS_COLOR)

    def _update_game(self, tick: float) -> None:
        """Update Game State.

        :param tick: Current tick in ms.
        """
        for event in pygame.event.get():
            handle_quit(event=event)
            self._snake.handle_event(event=event)

        self._snake.process_movement(tick=tick)
        self._snake.detect_collision(apple=self._apple)

    def _render_graphics(self) -> None:
        """Render the frame and display it in the screen."""
        layers = [
            (self._apple.surface, self._apple.render_pos),
            (self._snake.surface, self._snake.render_pos),
            (self._grid.surface, (0, 0)),
        ]
        if self._debug:
            layers.append((self._debug_surface, (0, 0)))

        self._screen.fill(color=self.BG_COLOR)
        self._screen.blits(layers)
        pygame.display.flip()
        self._render_clock.tick()

    def _main_loop(self) -> None:
        """Main Application Loop."""
        loops = 0
        current_tick = time_ms()
        while current_tick > self._next_tick and loops < self.MAX_FRAMESKIP:
            self._update_game(tick=current_tick)
            self._next_tick += self.TICK_STEP
            loops += 1

        self._render_graphics()

    def run(self) -> None:
        """Run the application."""
        while True:
            try:
                self._main_loop()
            except QuitApplication:
                break
