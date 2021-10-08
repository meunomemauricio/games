"""Define the Main Application class."""
from functools import cached_property

import pygame
from pygame.event import Event
from pygame.font import SysFont, get_default_font
from pygame.surface import Surface
from pygame.time import Clock

from games.projectile.projectile import ProjectileManager
from games.projectile.settings import (
    BG_COLOR,
    CAPTION,
    FPS_COLOR,
    FPS_SIZE,
    GRID_ALPHA,
    GRID_COLOR,
    GRID_WIDTH,
    MAX_FRAMESKIP,
    TICK_TIME,
)
from games.projectile.terrain import Blueprint, Terrain
from games.projectile.turret import Turret
from games.utils import time_ms


class QuitApplication(Exception):
    """Quit the application if raised inside the Main Loop."""


class MainApp:
    """Main Application."""

    def __init__(self, bp_name: str, debug: bool, grid: bool, show_fps: bool):
        """Main Application.

        :param bp_name: Name of the Blueprint to be loaded.
        :param debug: If `True`, display debug messages.
        :param grid: If `True`, draw a grid on top of the screen.
        :param show_fps: If `True`, render the FPS on screen.
        """
        self._debug = debug
        self._grid = grid
        self._show_fps = show_fps

        # Init PyGame
        pygame.init()
        pygame.display.set_caption(CAPTION)

        # Application Variables
        self._next_tick = time_ms()
        self._render_clock = Clock()
        self._running = True

        # Game Elements
        self._blueprint = Blueprint(name=bp_name)

        self._screen = pygame.display.set_mode(size=self._blueprint.rect.size)

        self._fps_font = SysFont(get_default_font(), FPS_SIZE)

        self._terrain = Terrain(blueprint=self._blueprint)

        self._proj_mgmt = ProjectileManager(blueprint=self._blueprint)
        self._hero = Turret(blueprint=self._blueprint, pm=self._proj_mgmt)

    @property
    def _fps_surface(self) -> Surface:
        """FPS Meter Surface."""
        msg = f"FPS: {self._render_clock.get_fps()}"
        return self._fps_font.render(msg, True, FPS_COLOR)

    @cached_property
    def _grid_surface(self) -> Surface:
        """A surface representing the Grid."""
        block_size = self._blueprint.block_size
        size = self._blueprint.rect.size
        surface = Surface(size=size, flags=pygame.SRCALPHA)
        surface.set_alpha(GRID_ALPHA)
        for x in range(0, size[0], int(block_size.x)):
            for y in range(0, size[1], int(block_size.y)):
                pygame.draw.rect(
                    surface=surface,
                    color=GRID_COLOR,
                    rect=pygame.Rect((x, y), self._blueprint.block_size),
                    width=GRID_WIDTH,
                )

        return surface

    def _handle_quit(self, event: Event) -> None:
        """Handle the Quit events.

        :param event: PyGame Event object.
        """
        if event.type == pygame.QUIT:
            raise QuitApplication
        elif event.type == pygame.KEYUP and event.key == pygame.K_q:
            raise QuitApplication

    def _update_game(self, tick: float) -> None:
        """Update Game State.

        :param tick: Current tick in ms.
        """
        for event in pygame.event.get():
            self._handle_quit(event=event)

        self._hero.process_logic(tick=tick)
        self._proj_mgmt.process_logic()

    def _calc_interpolation(self) -> float:
        """Calculate the Interpolation between game ticks."""
        next_prediction = time_ms() + TICK_TIME - self._next_tick
        interp = next_prediction / TICK_TIME
        return max(min(interp, 1.0), 0.0)  # Clip between 0 and 1

    def _render_graphics(self, interp: float) -> None:
        """Render the frame and display it in the screen.

        :param interp: To allow smoother movement on screen, interpolation is
          used when rendering the screen between game state updates,
        """
        layers = [
            (self._terrain.surface, (0, 0)),
            (self._proj_mgmt.build_surface(interp), (0, 0)),
            (self._hero.surface, self._hero.render_pos),
        ]
        if self._grid:
            layers.append((self._grid_surface, (0, 0)))

        if self._show_fps:
            layers.append((self._fps_surface, (0, 0)))

        self._screen.fill(color=BG_COLOR)
        self._screen.blits(layers)
        pygame.display.flip()
        self._render_clock.tick()

    def _main_loop(self) -> None:
        """Main Application Loop."""
        loops = 0
        current_tick = time_ms()
        while current_tick > self._next_tick and loops < MAX_FRAMESKIP:
            self._update_game(tick=current_tick)
            self._next_tick += TICK_TIME
            loops += 1

        interpolation = self._calc_interpolation()
        self._render_graphics(interp=interpolation)

    def run(self) -> None:
        """Run the application."""
        while True:
            try:
                self._main_loop()
            except QuitApplication:
                break
