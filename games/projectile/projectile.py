"""Define Projectiles and its manager."""
from typing import Optional, Set

import pygame
from pygame import draw
from pygame.color import Color
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from games.projectile.settings import SPEED_CONSTANT
from games.projectile.terrain import Blueprint


class ProjectileExploded(Exception):
    """Projectile hit something."""


class Projectile:
    """Projectile."""

    #: Earth's gravity (m/s²), adjusted to logic update rate.
    GRAVITY = Vector2(0, 9.78 * SPEED_CONSTANT)

    #: Drag Constant
    # TODO: Calculate for air.
    DRAG_CONSTANT = -0.4 * SPEED_CONSTANT

    def __init__(self, blueprint: Blueprint, velocity: Vector2, pos: Vector2):
        """Simulates a Projectile from the Turret.

        :param blueprint: Terrain Blueprint.
        :param velocity: Initial Velocity Vector.
        :param pos: Initial Position, in screen coordinates.
        """
        self._blueprint: Blueprint = blueprint
        self._curr_pos: Vector2 = pos

        self.velocity = Vector2(velocity)

    def _handle_oos_collision(self) -> None:
        """Out of Screen Collision Detection.

        :return `True` when the current position is not inside the screen.
        """
        if not self._blueprint.rect.collidepoint(
            self._curr_pos.x,
            self._curr_pos.y,
        ):
            raise ProjectileExploded

    def _handle_terrain_collision(self) -> None:
        """Detect collision with Terrain."""
        aaaa = self.rect.collidelist(self._blueprint.walls) > -1
        if aaaa:
            self.velocity.reflect_ip(Vector2(0, 1))

    @property
    def color(self) -> Color:
        """Projectile Color."""
        return Color(0xFF, 0xFF, 0x00)  # Yellow

    @property
    def radius(self) -> int:
        """Projectile Radius."""
        return 3

    @property
    def rect(self) -> Rect:
        # TODO: Is this aligned with the circle?
        return Rect(self._curr_pos, (self.radius * 2, self.radius * 2))

    def process_logic(self) -> None:
        """Process the Projectile logic and update its status."""
        drag = self.DRAG_CONSTANT * self.velocity
        self.velocity += self.GRAVITY + drag
        self._curr_pos += self.velocity

        self._handle_oos_collision()
        self._handle_terrain_collision()

    def get_render_position(self, interp: float) -> Vector2:
        """Calculate the Rendering Position, in screen coordinates.

        A linear interpolation is made between the current position and a
        prediction of the next position.
        """
        next_pos: Vector2 = self._curr_pos + self.velocity
        return self._curr_pos.lerp(next_pos, interp)


class ProjectileManager:
    """Projectile Manager."""

    def __init__(self, blueprint: Blueprint):
        """Manage and Render all projectiles.

        :param blueprint: Terrain Blueprint.
        """
        self._blueprint = blueprint
        self._projectiles: Set[Projectile] = set()

        self.latest: Optional[Projectile] = None

    def create_projectile(self, velocity: Vector2, pos: Vector2) -> None:
        """Create a Projectile and add it to the list.

        :param velocity: Initial Velocity.
        :param pos: Initial Position, in screen coordinates.
        """
        projectile = Projectile(
            blueprint=self._blueprint, velocity=velocity, pos=pos
        )
        self._projectiles.add(projectile)
        self._latest = projectile

    def process_logic(self) -> None:
        """Process logic and update status."""
        to_be_removed = set()
        for proj in self._projectiles:
            try:
                proj.process_logic()
            except ProjectileExploded:
                to_be_removed.add(proj)

        self._projectiles -= to_be_removed

    def build_surface(self, interp: float) -> Surface:
        """Fully rendered Surface."""
        sface = Surface(size=self._blueprint.rect.size, flags=pygame.SRCALPHA)
        for proj in self._projectiles:
            draw.circle(
                surface=sface,
                color=proj.color,
                center=proj.get_render_position(interp=interp),
                radius=proj.radius,
            )

        return sface
