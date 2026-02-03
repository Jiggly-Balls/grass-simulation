from __future__ import annotations

import functools
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from pygame import Surface

__all__ = ("get_sprite_sheet",)


@functools.cache
def get_sprite_sheet(path: str, tile_size: int) -> list[Surface]:
    sprite_sheet = pygame.image.load(path).convert()
    total_frames = sprite_sheet.get_size()[0] // tile_size
    images: list[Surface] = []

    for offset in range(total_frames):
        surf = pygame.Surface((tile_size, tile_size)).convert()
        total_offset = offset * tile_size
        surf.blit(
            sprite_sheet,
            area=(
                0 + total_offset,
                0,
                tile_size + total_offset,
                tile_size + total_offset,
            ),
        )
        surf.set_colorkey((0, 0, 0))
        width, height = surf.get_size()

        expanded_surf = pygame.transform.scale(
            surf, (width * 1.5, height * 1.5)
        )
        images.append(expanded_surf)

    return images
