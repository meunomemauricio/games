"""Define the Cannon entity."""
from pygame import draw
from pygame.math import Vector2
from pygame.surface import Surface

from snake.experimental.terrain import Blueprint


class Cannon:

    COLOR = (0xFF, 0x00, 0x00)

    def __init__(self, blueprint: Blueprint):
        """Cannon Entity.

        :param initial_pos: Initial Position of the Cannon.
        :param blueprint: Blueprint of the Terrain.
        """
        self._bp = blueprint

    @property
    def pos(self) -> Vector2:
        """Position in the Screen."""
        return Vector2(10, 10)

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
