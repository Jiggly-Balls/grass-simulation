from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from data.constants import TILE_SIZE

if TYPE_CHECKING:
    from pygame import Surface

__all__ = ("load_sprite_sheet",)


def load_sprite_sheet(path: str) -> list[Surface]:
    sprite_sheet = pygame.image.load(path).convert_alpha()
    total_frames = sprite_sheet.get_size()[0] // TILE_SIZE
    images: list[Surface] = []

    for offset in range(total_frames):
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE)).convert_alpha()
        total_offset = offset * TILE_SIZE
        surf.blit(
            sprite_sheet,
            area=(
                0 + total_offset,
                0,
                TILE_SIZE + total_offset,
                TILE_SIZE + total_offset,
            ),
        )
        surf.set_colorkey((0, 0, 0))
        width, height = surf.get_size()

        expanded_surf = pygame.transform.scale(
            surf, (width * 1.5, height * 1.5)
        )
        images.append(expanded_surf)

    return images
