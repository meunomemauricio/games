"""Define the Cannon entity."""
from typing import Optional

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

        self._loc: Optional[Vector2] = None
        self._pos: Optional[Vector2] = None

    def _find_in_blueprint(self) -> Vector2:
        """Determine the initial position using the Blueprint."""
        for y, row in enumerate(self._bp.terrain):
            x = row.find(self.CHAR)
            if x != -1:
                return Vector2(
                    x=x * self._bp.block_size[0],
                    y=y * self._bp.block_size[1],
                )

    @property
    def loc(self) -> Vector2:
        """Location in the Grid."""
        if self._loc is None:
            self._loc = self._find_in_blueprint()

        return self._loc

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
        surface = Surface(size=self._bp.block_size)
        draw.rect(
            surface=surface,
            color=self.COLOR,
            rect=((0, 0), self._bp.block_size),
        )
        return surface
