from __future__ import annotations

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
    def __init__(self, grass_objects: dict[G, Surface]) -> None:
        self.grass_objects: dict[G, Surface] = grass_objects

    def add(
        self, position: Vector2, grass_variants: None | Sequence[G] = None
    ) -> None: ...

    def draw(self, surface: Surface, offset: Vector2) -> None: ...
