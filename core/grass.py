from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from pygame import Rect, Surface, Vector2


class GrassSprite:
    def __init__(
        self,
        image: Surface,
        position: Vector2,
    ) -> None:
        self.image: Surface = image
        self.rect: Rect = image.get_rect()
        self.rect.center = position


class GrassGroup:
    def __init__(self) -> None:
        screen_size = pygame.display.get_surface()
        assert screen_size is not None

        self.surf_width: int
        self.surf_height: int
        self.surf_width, self.surf_height = screen_size.get_size()
        self.grass_surf: Surface = pygame.Surface(
            (self.surf_width, self.surf_height),
            # pygame.SRCALPHA,
        )
        self.grass_objects: list[GrassSprite] = []

    def add(self, grass_sprite: GrassSprite) -> None:
        self.grass_objects.append(grass_sprite)
        self.grass_objects.sort(key=lambda sprite: sprite.rect.y)

        # SELECTIVE REDRAWING-

        rect_size = self.grass_surf.get_rect()
        rect_size.topleft = grass_sprite.rect.topleft
        rect_size.width = 10
        pygame.draw.rect(
            self.grass_surf,
            (0, 0, 0),
            (*grass_sprite.rect.center, 10, 10),
        )

        for_redraw: list[tuple[Surface, Rect]] = [
            (sprite.image, sprite.rect)
            for sprite in self.grass_objects
            if grass_sprite.rect.x + 15
            > sprite.rect.x
            > grass_sprite.rect.x - 15
            # and
            # grass_sprite.rect.y + 10 > sprite.rect.y > grass_sprite.rect.y - 10
        ]
        for_redraw.sort(key=lambda source: source[1].y)

        # self.grass_surf.blits(
        #     (sprite.image, sprite.rect.topleft)
        #     for sprite in self.grass_objects
        #     if grass_sprite.rect.x + 30 > sprite.rect.x > grass_sprite.rect.x - 30
        #     and
        #     grass_sprite.rect.y + 30 > sprite.rect.y > grass_sprite.rect.y - 30
        # )
        self.grass_surf.blits(
            (sprite[0], sprite[1].topleft) for sprite in for_redraw
        )

        # NORMAL RENDERING-

        # self.grass_surf.blits(
        #     (sprite.image, sprite.rect.topleft)
        #     for sprite in self.grass_objects
        # )

    def draw(self, surface: Surface, offset: Vector2) -> None:
        # surface.blits(
        #     (spr.image, spr.rect.topleft + offset) for spr in self.sprites()
        # )
        surface.blit(
            self.grass_surf, self.grass_surf.get_rect().topleft + offset
        )
