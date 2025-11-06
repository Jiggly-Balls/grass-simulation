from __future__ import annotations

from typing import TYPE_CHECKING

from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface

if TYPE_CHECKING:
    from pygame import Rect, Surface, Vector2


class GrassSprite(Sprite):
    def __init__(
        self,
        group: Group[GrassSprite],
        image: Surface,
        position: Vector2,
    ) -> None:
        super().__init__(group)
        self.image: Surface = image
        self.rect: Rect = image.get_rect()
        self.rect.center = position


class GrassGroup(Group[GrassSprite]):
    def draw(self, surface: Surface, offset: Vector2) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        surface.blits(
            (spr.image, spr.rect.topleft + offset) for spr in self.sprites()
        )
