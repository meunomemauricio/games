import json
from functools import cached_property
from pathlib import Path
from typing import Dict, List, Tuple, Union

import pygame
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
    def block_size(self) -> Tuple[int, int]:
        """Size, in pixels, of a single block unit."""
        return (
            self._data["block"]["width"],
            self._data["block"]["height"],
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
    }

    def __init__(self, blueprint: Blueprint):
        self._bp = blueprint

    def draw_terrain(self) -> Surface:
        surface = Surface(self._bp.size)
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

    @cached_property
    def surface(self) -> Surface:
        """Fully drawn map as a Surface."""
        # TODO: Use .blits() when drawing many things
        terrain_surface = Surface(size=self._bp.size)
        terrain_surface.blit(source=self.draw_terrain(), dest=(0, 0))
        return terrain_surface