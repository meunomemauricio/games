"""Define Projectiles and its manager."""
from typing import List, Tuple

import pygame
from pygame import draw
from pygame.math import Vector2
from pygame.surface import Surface

from snake.experimental.terrain import Blueprint


class Projectile:
    """Projectile."""

    def __init__(self, blueprint: Blueprint, dir: Vector2, pos: Vector2):
        """Simulates a Projectile from the Turret.

        :param blueprint: Terrain Blueprint.
        :param pos: Initial Position, in screen coordinates.
        :param speed: Initial Speed Vector, in screen coordinates.
        """
        self._blueprint = blueprint
        self._dir = dir
        self._pos = pos

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

    @property
    def speed(self) -> float:
        return 1.0

    def process_logic(self) -> None:
        """Process the Projectile logic and update its status."""
        # TODO: Detect collisions
        # TODO: TOO F***ING QUICK!
        self._pos += self._dir * self.speed


class ProjectileManager:
    """Projectile Manager."""

    def __init__(self, blueprint: Blueprint):
        """Manage and Render all projectiles.

        :param blueprint: Terrain Blueprint.
        """
        self._blueprint = blueprint

        self._projectiles: List[Projectile] = []

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

    def create_projectile(self, dir: Vector2, pos: Vector2) -> None:
        """Create a Projectile and add it to the list.

        :param dir: Initial Direction, in screen coordinates.
        :param pos: Initial Position, in screen coordinates.
        """
        self._projectiles.append(
            Projectile(blueprint=self._blueprint, dir=dir, pos=pos)
        )

    def process_logic(self) -> None:
        """Process logic and update status."""
        for proj in self._projectiles:
            proj.process_logic()
