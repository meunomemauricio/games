"""Define Projectiles and its manager."""
from typing import List, Tuple

import pygame
from pygame import draw
from pygame.math import Vector2
from pygame.surface import Surface

from snake.experimental.terrain import Blueprint


class Projectile:
    """Projectile."""

    def __init__(self, blueprint: Blueprint, pos: Vector2, speed: Vector2):
        """Simulates a Projectile from the Turret.

        :param blueprint: Terrain Blueprint.
        :param pos: Initial Position, in screen coordinates.
        :param speed: Initial Speed Vector, in screen coordinates.
        """
        self._blueprint = blueprint
        self._pos = pos
        self._speed = speed

    @property
    def color(self) -> Tuple[int, int, int]:
        """Projectile Color."""
        return 0xFF, 0xFF, 0x00  # Yellow

    @property
    def pos(self) -> Vector2:
        """Current Position, in screen coordinates."""
        return self._pos

    @property
    def radius(self) -> int:
        """Projectile Radius."""
        return 5


class ProjectileManager:
    """Projectile Manager."""

    def __init__(self, blueprint: Blueprint):
        """Manage and Render all projectiles.

        :param blueprint: Terrain Blueprint.
        """
        self._blueprint = blueprint

        self._projectiles: List[Projectile] = []

    def create_projectile(self, pos: Vector2, speed: Vector2) -> None:
        """Create a Projectile and add it to the list.

        :param pos: Initial Position, in screen coordinates.
        :param speed: Initial Speed Vector, in screen coordinates.
        """
        print(f"{pos} | {speed}")
        self._projectiles.append(
            Projectile(blueprint=self._blueprint, pos=pos, speed=speed)
        )

    @property
    def surface(self) -> Surface:
        """Fully rendered Surface."""
        surface = Surface(size=self._blueprint.size, flags=pygame.SRCALPHA)
        for proj in self._projectiles:
            draw.circle(
                surface=surface,
                color=proj.color,
                center=proj.pos,
                radius=proj.radius,
            )

        return surface
