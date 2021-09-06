"""Define the Cannon entity."""
from typing import Optional

import pygame
from pygame import draw
from pygame.math import Vector2
from pygame.surface import Surface

from snake.experimental.terrain import Blueprint


class Cannon:

    COLOR = (0xFF, 0x00, 0x00)
    CHAR = "H"

    def __init__(self, blueprint: Blueprint):
        """Cannon Entity.

        :param initial_pos: Initial Position of the Cannon.
        :param blueprint: Blueprint of the Terrain.
        """
        self._bp = blueprint

        self._pos: Optional[Vector2] = None

        #: Location in the Grid.
        self.loc: Vector2 = self._find_in_blueprint()

        #: Aim Direction
        self.aim = Vector2()
        self.aim.from_polar((30, -45))

    def _find_in_blueprint(self) -> Vector2:
        """Determine the initial position using the Blueprint."""
        for i, row in enumerate(self._bp.terrain):
            try:
                return Vector2(x=row.index(self.CHAR), y=i)
            except ValueError:
                continue

    @property
    def pos(self) -> Vector2:
        """Position in the Screen."""
        return Vector2(
            x=self.loc.x * self._bp.block_size.x,
            y=self.loc.y * self._bp.block_size.y,
        )

    @property
    def surface(self) -> Surface:
        """Cannon Surface.

        It's drawn every time it's referenced.

        :return: Cannon Surface.
        """
        surface = Surface(size=self._bp.size, flags=pygame.SRCALPHA)
        draw.rect(  # Base
            surface=surface,
            color=self.COLOR,
            rect=(self.pos, self._bp.block_size),
        )
        draw.line(  # Aim
            surface=surface,
            color=self.COLOR,
            start_pos=self.pos + Vector2(25, 10),
            end_pos=self.pos + Vector2(25, 10) + self.aim,
            width=5,
        )
        return surface
