from functools import cached_property

import pygame
from pygame.surface import Surface

from snake.experimental.cannon import Cannon
from snake.experimental.terrain import Blueprint, Terrain


class MainApp:

    CAPTION = "Experimental v0.1"

    BG_COLOR = (0x00, 0x00, 0x00)

    GRID_COLOR = (0x55, 0x55, 0x55)
    GRID_WIDTH = 1

    def __init__(self, bp_name: str, grid: bool):
        """Main Application.

        :param bp_name: Name of the Blueprint to be loaded.
        :param grid: If `True`, draw a grid on top of the Screen.
        """
        pygame.init()
        pygame.display.set_caption(self.CAPTION)

        self._grid = grid
        self._running = True

        self._bp = Blueprint(name=bp_name)
        self._screen = pygame.display.set_mode(size=self._bp.size)
        self._terrain = Terrain(blueprint=self._bp)
        self._hero = Cannon(blueprint=self._bp)

    @cached_property
    def grid_surface(self) -> Surface:
        """A surface representing the Grid."""
        # FIXME: Grid has black background
        grid_surface = Surface(self._bp.size)
        for x in range(0, self._bp.size[0], self._bp.block_size[0]):
            for y in range(0, self._bp.size[1], self._bp.block_size[1]):
                pygame.draw.rect(
                    surface=grid_surface,
                    color=self.GRID_COLOR,
                    rect=pygame.Rect((x, y), self._bp.block_size),
                    width=self.GRID_WIDTH,
                )

        return grid_surface

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

    def handle_graphics(self) -> None:
        self._screen.fill(color=self.BG_COLOR)
        self._screen.blit(source=self._terrain.surface, dest=(0, 0))
        self._screen.blit(source=self._hero.surface, dest=self._hero.pos)
        if self._grid:
            self._screen.blit(source=self.grid_surface, dest=(0, 0))

        pygame.display.flip()

    def execute(self) -> None:
        while self._running:
            self.handle_input()
            self.handle_graphics()
