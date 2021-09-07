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

    INITIAL_ANGLE = -45

    CIRCLE_RATE = 1 / 6
    AIM_RATE = 1 / 3.4
    AIM_WIDTH = 10

    def __init__(self, blueprint: Blueprint):
        """Cannon Entity.

        :param initial_pos: Initial Position of the Cannon.
        :param blueprint: Blueprint of the Terrain.
        """
        self._bp = blueprint
        self._bs = self._bp.block_size  #: Block Size Shortcut

        self._pos: Optional[Vector2] = None

        #: Location in the Grid.
        self.loc: Vector2 = self._find_in_blueprint()

        #: Aim Direction
        self.aim = Vector2()
        self.aim.from_polar(
            (self._bs.length() * self.AIM_RATE, self.INITIAL_ANGLE)
        )

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
        return Vector2(x=self.loc.x * self._bs.x, y=self.loc.y * self._bs.y)

    @property
    def center(self) -> Vector2:
        """Center of the Cannon"""
        return Vector2(
            x=self._bs.x / 2,
            y=self._bs.y / 2,
        )

    @property
    def surface(self) -> Surface:
        """Cannon Surface.

        It's drawn every time it's referenced.

        :return: Cannon Surface.
        """
        surface = Surface(size=self._bs, flags=pygame.SRCALPHA)
        draw.circle(  # Base
            surface=surface,
            color=self.COLOR,
            center=self.center,
            radius=self._bs.length() * self.CIRCLE_RATE,
        )
        draw.line(  # Aim
            surface=surface,
            color=self.COLOR,
            start_pos=self.center,
            end_pos=self.center + self.aim,
            width=self.AIM_WIDTH,
        )
        return surface
