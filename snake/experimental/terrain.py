import json
from functools import cached_property
from pathlib import Path
from typing import Dict, List, Tuple, Union

import pygame
from pygame.math import Vector2
from pygame.surface import Surface

PINK = (0xFF, 0x00, 0xFF)
BLUEPRINT_DIR = Path(__file__).parent / "blueprints"

BPData = Dict[
    str, Union[int, str, dict, List[str]]
]  # TODO: Convert to dataclass
Color = Tuple[int, int, int]


class Blueprint:
    def __init__(self, name: str):
        self._name = name

        # TODO: Verify if all rows have same width

    @cached_property
    def _data(self) -> BPData:
        filepath = BLUEPRINT_DIR / f"{self._name}.json"
        with filepath.open() as fd:
            return json.load(fd)

    @property
    def name(self) -> str:
        """Blueprint Name."""
        return self._data["name"]

    @property
    def terrain(self) -> List[str]:
        """Terrain Coordinates."""
        return self._data["terrain"]

    @property
    def width(self) -> int:
        """Terrain Width."""
        return len(self.terrain[0])

    @property
    def height(self) -> int:
        """Terrain Height."""
        return len(self.terrain)

    @property
    def block_size(self) -> Vector2:
        """Size, in pixels, of a single block unit."""
        return Vector2(
            x=self._data["block"]["width"],
            y=self._data["block"]["height"],
        )

    @property
    def size(self) -> Tuple[int, int]:
        """Total Blueprint Size."""
        return (
            self.width * self._data["block"]["width"],
            self.height * self._data["block"]["height"],
        )


class Terrain:

    SPACE_CHAR = " "

    CHAR_MAPPING: Dict[str, Color] = {
        "*": (0xAA, 0xAA, 0xAA),
        "H": (0x00, 0x00, 0x00),
    }

    def __init__(self, blueprint: Blueprint):
        self._bp = blueprint

    @cached_property
    def surface(self) -> Surface:
        """Fully drawn map as a Surface."""
        surface = Surface(size=self._bp.size, flags=pygame.SRCALPHA)
        for j, row in enumerate(self._bp.terrain):
            for i, char in enumerate(row):
                if char == self.SPACE_CHAR:
                    continue

                pos = (i * self._bp.block_size[0], j * self._bp.block_size[1])
                pygame.draw.rect(
                    surface=surface,
                    color=self.CHAR_MAPPING.get(char, PINK),
                    rect=pygame.Rect(pos, self._bp.block_size),
                )

        return surface
