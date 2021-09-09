import time
from functools import cached_property

import pygame
from pygame.event import Event
from pygame.surface import Surface

from snake.experimental.projectile import ProjectileManager
from snake.experimental.terrain import Blueprint, Terrain
from snake.experimental.turret import Turret


def time_ms() -> float:
    """Simple wrapper to return current time in milliseconds."""
    return time.time() * 1000


class MainApp:

    #: Screen/Window parameters.
    CAPTION = "Experimental v0.1"
    BG_COLOR = (0x00, 0x00, 0x00)

    #: Grid Parameters
    GRID_COLOR = (0xFF, 0xFF, 0xFF)
    GRID_WIDTH = 1
    GRID_ALPHA = 50

    #: Difference in time between ticks
    TICK_STEP = 20.0  # ms

    #: Max number of rendered frames that can be skipped. This is mostly
    #  relevant on slower machines, in case the time it takes to update the
    #  game state is greater than `TICK_STEP`.
    MAX_FRAMESKIP = 10

    def __init__(self, bp_name: str, debug: bool, grid: bool):
        """Main Application.

        :param bp_name: Name of the Blueprint to be loaded.
        :param debug:
        :param grid: If `True`, draw a grid on top of the Screen.
        """
        pygame.init()
        pygame.display.set_caption(self.CAPTION)

        self._debug = debug
        self._grid = grid

        # Main Loop Variables
        self._running = True
        self._next_tick = time_ms()

        self._blueprint = Blueprint(name=bp_name)

        self._screen = pygame.display.set_mode(size=self._blueprint.rect.size)

        self._terrain = Terrain(blueprint=self._blueprint)

        self._proj_mgmt = ProjectileManager(blueprint=self._blueprint)
        self._hero = Turret(blueprint=self._blueprint, pm=self._proj_mgmt)

    @cached_property
    def grid_surface(self) -> Surface:
        """A surface representing the Grid."""
        block_size = self._blueprint.block_size
        size = self._blueprint.rect.size
        surface = Surface(size=size, flags=pygame.SRCALPHA)
        surface.set_alpha(self.GRID_ALPHA)
        for x in range(0, size[0], int(block_size.x)):
            for y in range(0, size[1], int(block_size.y)):
                pygame.draw.rect(
                    surface=surface,
                    color=self.GRID_COLOR,
                    rect=pygame.Rect((x, y), self._blueprint.block_size),
                    width=self.GRID_WIDTH,
                )

        return surface

    def _handle_quit(self, event: Event) -> None:
        """Handle the Quit events.

        :param event: PyGame Event object.
        """
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_q:
            self._running = False

    def _handle_input(self) -> None:
        for event in pygame.event.get():
            self._hero.handle_event(event=event)
            self._handle_quit(event=event)

    def _process_logic(self) -> None:
        self._proj_mgmt.process_logic()

    def _update_game(self) -> None:
        """Update Game State."""
        self._handle_input()
        self._process_logic()

    def _calc_interpolation(self) -> float:
        """Calculate the Interpolation between game ticks."""
        return (time_ms() + self.TICK_STEP - self._next_tick) / self.TICK_STEP

    def _render_graphics(self, interpolation: float) -> None:
        if self._debug:
            print(interpolation)

        layers = [
            (self._terrain.surface, (0, 0)),
            (self._proj_mgmt.surface, (0, 0)),
            (self._hero.surface, self._hero.render_pos),
        ]
        if self._grid:
            layers.append((self.grid_surface, (0, 0)))

        self._screen.fill(color=self.BG_COLOR)
        self._screen.blits(layers)
        pygame.display.flip()

    def _main_loop(self) -> None:
        loops = 0
        while time_ms() > self._next_tick and loops < self.MAX_FRAMESKIP:
            self._update_game()
            self._next_tick += self.TICK_STEP
            loops += 1

        interpolation = self._calc_interpolation()
        self._render_graphics(interpolation=interpolation)

    def run(self) -> None:
        while self._running:
            self._main_loop()
