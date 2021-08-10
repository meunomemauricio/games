"""Main."""

import pygame
from pygame.rect import Rect

from snake.snake import Snake


class MainApp:

    CAPTION = "Snake v0.1"

    WIDTH = 1000
    HEIGHT = 1000

    BG_COLOR = (0x00, 0x00, 0x00)

    GRID_SIZE = 100
    GRID_COLOR = (0xFF, 0x00, 0x00)
    GRID_WIDTH = 1

    def __init__(self):
        pygame.init()

        # TODO: Add Logo
        pygame.display.set_caption(self.CAPTION)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.snake = Snake()

    def draw_grid(self):
        for x in range(0, self.WIDTH, self.GRID_SIZE):
            for y in range(0, self.HEIGHT, self.GRID_SIZE):
                pygame.draw.rect(
                    surface=self.screen,
                    color=self.GRID_COLOR,
                    rect=Rect(x, y, self.GRID_SIZE, self.GRID_SIZE),
                    width=self.GRID_WIDTH,
                )

    def execute(self):
        running = True
        while running:
            self.screen.fill(color=self.BG_COLOR)
            self.draw_grid()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.blit(source=self.snake.sprite, dest=self.snake.pos)

            self.snake.inc_x()
            self.snake.inc_y()

            pygame.display.flip()
