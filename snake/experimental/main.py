from functools import cached_property

import pygame
from pygame.surface import Surface


class MainApp:

    CAPTION = "Experimental v0.1"

    WIDTH = 1000
    HEIGHT = 1000

    BG_COLOR = (0x00, 0x00, 0x00)

    GRID_SIZE = 100
    GRID_COLOR = (0x55, 0x55, 0x55)
    GRID_WIDTH = 1

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(self.CAPTION)

        self._running = True

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    @cached_property
    def grid_surface(self) -> Surface:
        """A surface representing the Grid."""
        grid_surface = Surface(self.screen.get_size())
        for x in range(0, self.WIDTH, self.GRID_SIZE):
            for y in range(0, self.HEIGHT, self.GRID_SIZE):
                pygame.draw.rect(
                    surface=grid_surface,
                    color=self.GRID_COLOR,
                    rect=pygame.Rect(x, y, self.GRID_SIZE, self.GRID_SIZE),
                    width=self.GRID_WIDTH,
                )

        return grid_surface

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

    def handle_graphics(self):
        self.screen.fill(color=self.BG_COLOR)
        self.screen.blit(source=self.grid_surface, dest=(0, 0))

        pygame.display.flip()

    def execute(self):
        while self._running:
            self.handle_input()
            self.handle_graphics()
