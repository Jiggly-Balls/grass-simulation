from __future__ import annotations

import bisect
import random
from collections import defaultdict
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
        self._spatial_grid: dict[tuple[int, int], list[Vector2]] = defaultdict(
            list
        )

        print(self._gap)

    def add(
        self,
        position: Vector2,
        tile_size: tuple[int, int] = (1, 1),
        grass_variants: None | Sequence[G] = None,
    ) -> None:
        if tile_size != (1, 1):
            for x in range(0, tile_size[0] * self._gap, self._gap):
                for y in range(0, tile_size[1] * self._gap, self._gap):
                    vec = pygame.Vector2(position.x + x, position.y + y)
                    self.add(vec)

        spatial_position: tuple[int, int] = self._lock_grid(
            (int(position.x), int(position.y))
        )
        for grid_cell in self._get_boundaries(spatial_position):
            for vector in self._spatial_grid[grid_cell]:
                if (position - vector).magnitude() < self._gap:
                    print("COLLISION")
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
        self._spatial_grid[
            self._lock_grid((int(position.x), int(position.y)))
        ].append(position)

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

    def _get_boundaries(
        self, position: tuple[int, int]
    ) -> tuple[
        tuple[int, int],
        tuple[int, int],
        tuple[int, int],
        tuple[int, int],
        tuple[int, int],
        tuple[int, int],
        tuple[int, int],
        tuple[int, int],
        tuple[int, int],
    ]:
        x, y = position
        # fmt: off
        grid = (
            ((x - 1) * self._gap, (y + 1) * self._gap), (x * self._gap, (y + 1) * self._gap), ((x + 1) * self._gap, (y + 1) * self._gap),
            ((x - 1) * self._gap, (y    ) * self._gap), (x            , (y    )            ), ((x + 1) * self._gap, (y    ) * self._gap),
            ((x - 1) * self._gap, (y - 1) * self._gap), (x * self._gap, (y - 1) * self._gap), ((x + 1) * self._gap, (y - 1) * self._gap),
        )
        # fmt: on

        return grid
