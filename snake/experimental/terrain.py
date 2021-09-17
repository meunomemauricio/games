import json
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Dict, List, Tuple, Union

import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from snake.utils import PINK

BLUEPRINT_DIR = Path(__file__).parent / "blueprints"

BPData = Dict[
    str, Union[int, str, dict, List[str]]
]  # TODO: Convert to dataclass
Color = Tuple[int, int, int]


class BlockType(str, Enum):

    HERO = "H"
    SPACE = " "
    WALL = "|"


class Block:
    def __init__(self, x: int, y: int, block_size: Vector2, block_type: str):
        self.x = x
        self.y = y
        self.block_size = block_size
        self.type = BlockType(block_type)

    @cached_property
    def rect(self) -> Rect:
        x_y = (self.x * self.block_size.x, self.y * self.block_size.y)
        return Rect(x_y, self.block_size)


class Blueprint:
    """Terrain Blueprint."""

    def __init__(self, name: str):
        """Represent the Terrain as a blueprint."""
        self._name = name

        # TODO: Verify if all rows have same width

    @cached_property
    def _data(self) -> BPData:
        filepath = BLUEPRINT_DIR / f"{self._name}.json"
        with filepath.open() as fd:
            return json.load(fd)

    @property
    def block_size(self) -> Vector2:
        """Size of a single block unit."""
        return Vector2(
            x=self._data["block"]["width"],
            y=self._data["block"]["height"],
        )

    @property
    def height(self) -> int:
        """Terrain Height."""
        return len(self.terrain)

    @property
    def name(self) -> str:
        """Blueprint Name."""
        return self._data["name"]

    @property
    def rect(self) -> Rect:
        """Rectangle with total size of the Blueprint."""
        return Rect(
            0,
            0,
            self.width * self._data["block"]["width"],
            self.height * self._data["block"]["height"],
        )

    @property
    def terrain(self) -> List[str]:
        """Terrain Coordinates."""
        return self._data["terrain"]

    @cached_property
    def blocks(self) -> Tuple[Block]:
        blocks = []
        for j, row in enumerate(self.terrain):
            for i, _type in enumerate(row):
                blocks.append(
                    Block(
                        x=i, y=j, block_size=self.block_size, block_type=_type
                    )
                )

        return tuple(blocks)

    @cached_property
    def walls(self) -> Tuple[Rect]:
        return tuple(
            blk.rect for blk in self.blocks if blk.type == BlockType.WALL
        )

    @property
    def width(self) -> int:
        """Terrain Width."""
        return len(self.terrain[0])


class Terrain:
    """Terrain Renderer."""

    SPACE_CHAR = " "

    COLLOR_MAPPING: Dict[str, Color] = {
        "|": (0xAA, 0xAA, 0xAA),
        "H": (0x00, 0x00, 0x00),
    }

    def __init__(self, blueprint: Blueprint):
        """Render the Terrain, following the Blueprint."""
        self._bp = blueprint

    @cached_property
    def surface(self) -> Surface:
        """Fully drawn map as a Surface."""
        surface = Surface(size=self._bp.rect.size, flags=pygame.SRCALPHA)
        for j, row in enumerate(self._bp.terrain):
            for i, char in enumerate(row):
                if char == self.SPACE_CHAR:
                    continue

                pos = (i * self._bp.block_size[0], j * self._bp.block_size[1])
                pygame.draw.rect(
                    surface=surface,
                    color=self.COLLOR_MAPPING.get(char, PINK),
                    rect=pygame.Rect(pos, self._bp.block_size),
                )

        return surface
