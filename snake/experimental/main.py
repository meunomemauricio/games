from functools import cached_property

import pygame
from pygame.event import Event
from pygame.surface import Surface

from snake.experimental.projectile import ProjectileManager
from snake.experimental.terrain import Blueprint, Terrain
from snake.experimental.turret import Turret


class MainApp:

    CAPTION = "Experimental v0.1"

    BG_COLOR = (0x00, 0x00, 0x00)

    GRID_COLOR = (0xFF, 0xFF, 0xFF)
    GRID_WIDTH = 1
    GRID_ALPHA = 50

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

        self._running = True

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

    def handle_input(self) -> None:
        for event in pygame.event.get():
            self._hero.handle_event(event=event)
            self._handle_quit(event=event)

    def process_logic(self) -> None:
        self._proj_mgmt.process_logic()

    def render_graphics(self) -> None:
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

    def execute(self) -> None:
        while self._running:
            self.handle_input()
            self.process_logic()
            self.render_graphics()
