"""Main."""
import pygame
from pygame.rect import Rect

from snake.snake import Snake
from snake.utils import time_ms


class MainApp:
    """Main application."""

    CAPTION = "Snake v0.1"

    WIDTH = 800
    HEIGHT = 800

    BG_COLOR = (0x00, 0x00, 0x00)

    GRID_SIZE = 20
    GRID_COLOR = (0xFF, 0x00, 0x00)
    GRID_WIDTH = 1

    TICK_STEP = 20.0

    def __init__(self):
        self._running = True
        self._next_tick: float = time_ms()

        pygame.init()

        # TODO: Add Logo
        pygame.display.set_caption(self.CAPTION)

        self._screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self._snake = Snake(grid_size=self.GRID_SIZE)

    def draw_grid(self) -> None:
        """Draw grid."""
        for x in range(0, self.WIDTH, self.GRID_SIZE):
            for y in range(0, self.HEIGHT, self.GRID_SIZE):
                pygame.draw.rect(
                    surface=self._screen,
                    color=self.GRID_COLOR,
                    rect=Rect(x, y, self.GRID_SIZE, self.GRID_SIZE),
                    width=self.GRID_WIDTH,
                )

    def handle_events(self) -> None:
        """Handle events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self._snake.move_y(step=-1)
                if event.key == pygame.K_DOWN:
                    self._snake.move_y(step=1)
                if event.key == pygame.K_RIGHT:
                    self._snake.move_x(step=1)
                if event.key == pygame.K_LEFT:
                    self._snake.move_x(step=-1)

    def render_screen(self) -> None:
        """Render the screen."""
        self._screen.fill(color=self.BG_COLOR)
        self.draw_grid()
        self._snake.draw(surface=self._screen)
        pygame.display.flip()

    def execute(self):
        """Application main loop."""
        while self._running:
            if time_ms() > self._next_tick:
                self.handle_events()
                self._next_tick += self.TICK_STEP

            self.render_screen()
