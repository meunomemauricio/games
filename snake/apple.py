"""Snake's favorite(?) food."""

from pygame.color import Color

from snake.elements import GridElement, RandomPoint


class Apple(GridElement):
    """Apple."""

    #: Apple Color
    COLOR = Color(0xFF, 0x00, 0x00)

    def __str__(self) -> str:
        return f"Apple: p={self.p}"

    def respawn(self) -> None:
        """Shuffle the Apple position."""
        self.p = RandomPoint(grid=self._grid)
