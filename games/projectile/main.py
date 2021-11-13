"""Define the Main Application class."""
from functools import cached_property
from typing import Iterable

import pygame
from pygame.event import Event
from pygame.font import SysFont, get_default_font
from pygame.surface import Surface

from games.application import GameApplication
from games.projectile.projectile import ProjectileManager
from games.projectile.settings import (
    BG_COLOR,
    FPS_COLOR,
    FPS_SIZE,
    GRID_ALPHA,
    GRID_COLOR,
    GRID_WIDTH,
    PIXEL_SIZE,
    SPEED_CONSTANT,
    TICK_STEP,
)
from games.projectile.terrain import Blueprint, Terrain
from games.projectile.turret import Turret
from games.snake.settings import DEBUG_COLOR
from games.utils import Layer, multi_text


class MainApp(GameApplication):
    """Main Application."""

    CAPTION = "Projectile v0.1"
    TICK_STEP = TICK_STEP

    def __init__(self, bp_name: str, debug: bool, grid: bool, show_fps: bool):
        """Main Application.

        :param bp_name: Name of the Blueprint to be loaded.
        :param debug: If `True`, display debug messages.
        :param grid: If `True`, draw a grid on top of the screen.
        :param show_fps: If `True`, render the FPS on screen.
        """
        super().__init__()

        self._debug = debug
        self._grid = grid
        self._show_fps = show_fps and not debug

        # Game Elements
        self._blueprint = Blueprint(name=bp_name)

        self._fps_font = SysFont(get_default_font(), FPS_SIZE)

        self._terrain = Terrain(blueprint=self._blueprint)

        self._proj_mgmt = ProjectileManager(blueprint=self._blueprint)
        self._hero = Turret(blueprint=self._blueprint, pm=self._proj_mgmt)

    @property
    def _debug_surface(self) -> Iterable[Layer]:
        """Debug Message Layers."""
        msgs = [
            f"FPS: {self._render_clock.get_fps()}",
            f"Block Size (m): {self._blueprint.block_size * PIXEL_SIZE}",
            f"Width: {self._blueprint.width * PIXEL_SIZE} m",
            f"Height: {self._blueprint.height * PIXEL_SIZE} m",
            f"Initial Speed: {self._hero.speed / SPEED_CONSTANT} m/s",
        ]
        latest = self._proj_mgmt.latest
        if latest:
            msgs.append(f"Proj. Velocity: {latest.velocity}")

        return multi_text(font=self._fps_font, color=DEBUG_COLOR, msgs=msgs)

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

    def _create_screen(self) -> Surface:
        """Create screen surface based on the Blueprint."""
        return pygame.display.set_mode(size=self._blueprint.rect.size)

    def _handle_events(self, event: Event) -> None:
        """No custom events to handle."""

    def _handle_updates(self, tick: float) -> None:
        """Handle updates to the game state."""
        self._hero.process_logic(tick=tick)
        self._proj_mgmt.process_logic()

    def _draw_graphics(self, interp: float) -> None:
        """Draw contents of the frame to the Screen."""
        layers = [
            (self._terrain.surface, (0, 0)),
            (self._proj_mgmt.build_surface(interp), (0, 0)),
            (self._hero.surface, self._hero.render_pos),
        ]
        if self._grid:
            layers.append((self._grid_surface, (0, 0)))

        if self._debug:
            layers.extend(self._debug_surface)

        if self._show_fps:
            layers.append((self._fps_surface, (0, 0)))

        self._screen.fill(color=BG_COLOR)
        self._screen.blits(layers)
