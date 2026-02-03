from __future__ import annotations

import bisect
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

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
    def __init__(self, grass_objects: dict[G, Surface], gap: int = 10) -> None:
        self.grass_objects: dict[G, Surface] = grass_objects
        self.sprites: list[GrassSprite[G]] = []
        self.gap: int = gap

    def add(
        self,
        position: Vector2,
        tile_size: tuple[int, int] = (1, 1),
        grass_variants: None | Sequence[G] = None,
    ) -> None:
        if grass_variants is None:
            grass_id = random.choice(tuple(self.grass_objects.keys()))
        else:
            grass_id = random.choice(grass_variants)

        bisect.insort(
            self.sprites,
            GrassSprite(grass_id, position),
            key=lambda grass_sprite: grass_sprite.position.y,
        )

    def draw(self, surface: Surface, offset: Vector2) -> None:
        data = (
            (self.grass_objects[sprite.image_id], sprite.position + offset)
            for sprite in self.sprites
        )
        surface.blits(data)
