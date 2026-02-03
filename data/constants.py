from __future__ import annotations

from enum import StrEnum, auto

__all__ = (
    "FPS",
    "SCREEN_RESOLUTION",
    "BASE_ASSET_PATH",
    "GRASS_SPRITE_SHEET",
    "GRASS_SPACING",
)

FPS: int = 60
GRASS_ABUNDANCE: int = 200
SCREEN_RESOLUTION: tuple[int, int] = (1000, 600)
SPEED: int = 500

BASE_ASSET_PATH = "assets/"
GRASS_SPRITE_SHEET = BASE_ASSET_PATH + "grass.png"
GRASS_SPACING: int = 15


class WorldEnum(StrEnum):
    MAIN_GAME = auto()
