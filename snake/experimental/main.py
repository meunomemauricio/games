import pygame

from snake.experimental.cannon import Cannon
from snake.experimental.terrain import Blueprint, Terrain


class MainApp:

    CAPTION = "Experimental v0.1"

    BG_COLOR = (0x00, 0x00, 0x00)

    def __init__(self, bp_name: str, grid: bool):
        """Main Application.

        :param bp_name: Name of the Blueprint to be loaded.
        :param grid: If `True`, draw a grid on top of the Screen.
        """
        pygame.init()
        pygame.display.set_caption(self.CAPTION)

        self._running = True

        blueprint = Blueprint(name=bp_name)
        self.screen = pygame.display.set_mode(size=blueprint.size)
        self.terrain = Terrain(blueprint=blueprint, grid=grid)
        self.hero = Cannon(blueprint=blueprint)

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

    def handle_graphics(self) -> None:
        self.screen.fill(color=self.BG_COLOR)
        self.screen.blit(source=self.terrain.surface, dest=(0, 0))
        self.screen.blit(source=self.hero.surface, dest=self.hero.pos)
        pygame.display.flip()

    def execute(self) -> None:
        while self._running:
            self.handle_input()
            self.handle_graphics()
