from __future__ import annotations

from enum import IntEnum, StrEnum, auto

__all__ = (
    "FPS",
    "TILE_SIZE",
    "SCREEN_RESOLUTION",
    "BASE_ASSET_PATH",
    "GRASS_SPRITE_SHEET",
    "GRASS_SPACING",
)

FPS: int = 60
TILE_SIZE: int = 32
SCREEN_RESOLUTION: tuple[int, int] = (1000, 600)

BASE_ASSET_PATH = "assets/"
GRASS_SPRITE_SHEET = BASE_ASSET_PATH + "grass.png"
GRASS_SPACING: int = 15


class WorldEnum(StrEnum):
    MAIN = auto()


class ProcessorPriority(IntEnum):
    MOVEMENT = 0
