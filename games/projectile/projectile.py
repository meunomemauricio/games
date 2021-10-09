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
from games.utils import time_ms


class ProjectileExploded(Exception):
    """Projectile hit something."""


class Projectile:
    """Projectile."""

    #: Projectile Color.
    COLOR = Color(0xFF, 0x00, 0x00)

    #: Earth's gravity (m/s²), adjusted to logic update rate.
    GRAVITY = Vector2(0, 9.78 * SPEED_CONSTANT)

    #: Drag Constant
    # TODO: Calculate for air.
    DRAG_CONSTANT = -0.4 * SPEED_CONSTANT

    #: Time (ms) for the
    EXPLOSION_TIME = 15000

    #: Coeffient of Restitution
    COR = 0.45

    def __init__(self, blueprint: Blueprint, velocity: Vector2, pos: Vector2):
        """Simulates a Projectile from the Turret.

        :param blueprint: Terrain Blueprint.
        :param velocity: Initial Velocity Vector.
        :param pos: Initial Position, in screen coordinates.
        """
        self._blueprint: Blueprint = blueprint
        self._curr_pos: Vector2 = pos

        self._explosion_time = time_ms() + self.EXPLOSION_TIME

        self.velocity = Vector2(velocity)

    def _detect_floor_collision(self) -> None:
        """Detect if there was a collision with the floor."""
        if self._curr_pos.y >= self._blueprint.rect.height:
            self._handle_reflection(normal=Vector2(1, 0))

    def _detect_terrain_collision(self) -> None:
        """Detect collision with Terrain."""
        walls = self._blueprint.walls
        col_index = self.rect.collidelist(walls)
        if col_index < 0:
            return

        normal = self._find_normal(pos=self._curr_pos, wall=walls[col_index])
        self._handle_reflection(normal=normal)

    def _find_normal(self, pos: Vector2, wall: Rect) -> Vector2:
        """Find the reflection normal based on which wall surface collided."""
        edges = (
            wall.topleft,
            wall.topright,
            wall.bottomleft,
            wall.bottomright,
        )
        points = (Vector2(e) for e in edges)
        # Sort the vectors by their length to the current position.
        sorted_points = sorted(points, key=lambda v: pos.distance_to(v))
        # Get the 2 closest points
        point_a, point_b = sorted_points[:2]
        # Make a vector between them. This is the surface that collided.
        # Rotate 90° to get the normal.
        return (point_b - point_a).rotate(90)

    def _handle_explosion_timer(self):
        """Explode the projectile when its timer is due."""
        if time_ms() > self._explosion_time:
            raise ProjectileExploded

    def _handle_movement(self):
        """Handle the Movement calculations."""
        drag = self.DRAG_CONSTANT * self.velocity
        self.velocity += self.GRAVITY + drag
        if self.velocity.length() <= 0.05:
            raise ProjectileExploded

        self._curr_pos += self.velocity

    def _handle_reflection(self, normal: Vector2):
        """Reflect the projectile against a normal vector."""
        self.velocity.reflect_ip(normal)
        self.velocity *= self.COR

    @property
    def radius(self) -> int:
        """Projectile Radius."""
        return 3

    @property
    def rect(self) -> Rect:
        rect = Rect((0, 0), (self.radius * 2, self.radius * 2))
        rect.center = self._curr_pos
        return rect

    def process_logic(self) -> None:
        """Process the Projectile logic and update its status."""
        self._handle_explosion_timer()
        self._handle_movement()
        self._detect_floor_collision()
        self._detect_terrain_collision()

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
        self.latest = projectile

    def process_logic(self) -> None:
        """Process logic and update status."""
        to_be_removed = set()
        for proj in self._projectiles:
            try:
                proj.process_logic()
            except ProjectileExploded:
                to_be_removed.add(proj)
                if self.latest == proj:
                    self.latest = None

        self._projectiles -= to_be_removed

    def build_surface(self, interp: float) -> Surface:
        """Fully rendered Surface."""
        sface = Surface(size=self._blueprint.rect.size, flags=pygame.SRCALPHA)
        for proj in self._projectiles:
            draw.circle(
                surface=sface,
                color=proj.COLOR,
                center=proj.get_render_position(interp=interp),
                radius=proj.radius,
            )

        return sface
