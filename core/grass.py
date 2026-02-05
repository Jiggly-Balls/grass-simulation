from __future__ import annotations

import bisect
import random
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from collections.abc import Generator, Sequence

    from pygame import Surface, Vector2


class GrassSprite[G: str | int]:
    def __init__(
        self,
        image_id: G,
        position: Vector2,
    ) -> None:
        self.image_id: G = image_id
        self.position: Vector2 = position


class GrassManager[G: str | int]:
    def __init__(self, grass_objects: dict[G, Surface], gap: int = 15) -> None:
        if gap < 0:
            raise ValueError(
                f"Expected `gap` argument to be a positive value. Instead got {gap=}"
            )

        self.grass_objects: dict[G, Surface] = grass_objects
        self.sprites: list[GrassSprite[G]] = []
        self._gap: int = gap
        self._gap_records: set[tuple[int, int]] = set[tuple[int, int]]()

        print(self._gap)

    def add(
        self,
        position: Vector2,
        tile_size: tuple[int, int] = (1, 1),
        grass_variants: None | Sequence[G] = None,
    ) -> None:
        if tile_size != (1, 1):
            for x in range(tile_size[0]):
                for y in range(tile_size[1]):
                    vec = pygame.Vector2(position.x + x, position.y + y)
                    self.add(vec)

        gap_grid = self._lock_grid((int(position.x), int(position.y)))
        if gap_grid in self._gap_records:
            return

        if grass_variants is None:
            grass_id = random.choice(tuple(self.grass_objects.keys()))
        else:
            grass_id = random.choice(grass_variants)

        bisect.insort(
            self.sprites,
            GrassSprite(grass_id, position),
            key=lambda grass_sprite: grass_sprite.position.y,
        )

        self._gap_records.add(gap_grid)

        print(f"PLACED {len(self.sprites)} GRASS BLADES")

    def draw(self, surface: Surface, offset: Vector2) -> None:
        data: Generator[tuple[Surface, Vector2], None, None] = (
            (self.grass_objects[sprite.image_id], sprite.position + offset)
            for sprite in self.sprites
        )
        surface.blits(data)

    def _lock_grid(self, pos: tuple[int, int]) -> tuple[int, int]:
        return (
            round(pos[0] / self._gap) * self._gap,
            round(pos[1] / self._gap) * self._gap,
        )
