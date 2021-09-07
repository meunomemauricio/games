"""Define the Turret entity."""
from typing import Callable, Optional

import pygame
from pygame import draw
from pygame.event import Event
from pygame.math import Vector2
from pygame.surface import Surface

from snake.experimental.projectile import ProjectileManager
from snake.experimental.terrain import Blueprint


class Turret:

    COLOR = (0xFF, 0x00, 0x00)
    CHAR = "H"

    INITIAL_ANGLE = -45
    AIM_SENSITIVITY = 10

    CIRCLE_RATE = 1 / 6
    AIM_RATE = 1 / 3.4
    AIM_WIDTH = 10

    def __init__(self, blueprint: Blueprint, pm: ProjectileManager):
        """Turret Entity.

        :param initial_pos: Initial Position of the Turret.
        :param blueprint: Blueprint of the Terrain.
        """
        self._bp = blueprint
        self._pm = pm
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

    def _decrease_angle(self) -> None:
        """Decrease Aim's Angle."""
        self.aim = self.aim.rotate(self.AIM_SENSITIVITY)

    def _increase_angle(self) -> None:
        """Increase Aim's Angle."""
        self.aim = self.aim.rotate(-self.AIM_SENSITIVITY)

    def _fire_turret(self) -> None:
        """Fire a Projectile from the Turret."""
        self._pm.create_projectile(dir=self.aim, pos=self.pos)

    @property
    def center(self) -> Vector2:
        """Turret Center, in local coordinates."""
        return Vector2(x=self._bs.x / 2, y=self._bs.y / 2)

    @property
    def pos(self) -> Vector2:
        """Current Position (center), in screen coordinates."""
        return self.render_pos + self.center

    @property
    def radius(self) -> float:
        """Turret Radius."""
        return self._bs.length() * self.CIRCLE_RATE

    @property
    def render_pos(self) -> Vector2:
        """Render Position, in screen coordinates."""
        return Vector2(x=self.loc.x * self._bs.x, y=self.loc.y * self._bs.y)

    @property
    def surface(self) -> Surface:
        """Turret Surface.

        It's drawn every time it's referenced.

        :return: Turret Surface.
        """
        surface = Surface(size=self._bs, flags=pygame.SRCALPHA)
        draw.circle(  # Base
            surface=surface,
            color=self.COLOR,
            center=self.center,
            radius=self.radius,
        )
        draw.line(  # Aim
            surface=surface,
            color=self.COLOR,
            start_pos=self.center,
            end_pos=self.center + self.aim,
            width=self.AIM_WIDTH,
        )
        return surface

    def handle_event(self, event: Event):
        """Handle the Hero events.

        :param event: Pygame Event object.
        """
        if event.type != pygame.KEYDOWN:
            return

        action: Callable = {
            pygame.K_RIGHT: self._decrease_angle,
            pygame.K_LEFT: self._increase_angle,
            pygame.K_SPACE: self._fire_turret,
        }.get(event.key)
        if action:
            action()
