"""Represent the main protagonist."""
from typing import Tuple

import pygame
from pygame import Surface
from pygame.rect import Rect


class Snake:
    """Snake."""

    SPRITE = "icon2.png"
    HEAD_COLOR = (0x00, 0xFF, 0x00)

    def __init__(self, grid_size: int):
        self._x: int = 0
        self._y: int = 0
        self._grid_size = grid_size

    @property
    def pos(self) -> Tuple[int, int]:
        return self._x, self._y

    def inc_x(self):
        self._x += 1

    def inc_y(self):
        self._y += 1

    def draw(self, surface: Surface):
        """Draw the snake on the surface."""
        pygame.draw.rect(
            surface=surface,
            color=self.HEAD_COLOR,
            rect=Rect(0, 0, self._grid_size, self._grid_size),
        )
