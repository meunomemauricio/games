"""Represent the main protagonist."""
from typing import Tuple

import pygame


class Snake:
    """Snake."""

    SPRITE = "icon2.png"

    def __init__(self):
        self._x: int = 0
        self._y: int = 0

        self.sprite = pygame.image.load(self.SPRITE)

    @property
    def pos(self) -> Tuple[int, int]:
        return self._x, self._y

    def inc_x(self):
        self._x += 1

    def inc_y(self):
        self._y += 1
