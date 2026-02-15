from __future__ import annotations

import random
from collections import defaultdict
from typing import TYPE_CHECKING

import pygame
from pygame.math import Vector2
from pygame.rect import FRect
from pygame.surface import Surface

from core.utils import BinaryGrassTree

if TYPE_CHECKING:
    from collections.abc import Generator, Sequence

    from pygame import FRect, Surface, Vector2


class GrassSprite[G: str | int]:
    __slots__: tuple[str, ...] = ("image_id", "position")

    def __init__(
        self,
        image_id: G,
        position: Vector2,
    ) -> None:
        self.image_id: G = image_id
        self.position: Vector2 = position
        # print(self.position)


class GrassManager[G: str | int]:
    def __init__(
        self,
        grass_objects: dict[G, Surface],
        camera_width: int,
        camera_height: int,
        gap: int = 17,
    ) -> None:
        if gap < 0:
            raise ValueError(
                f"Expected `gap` argument to be a non-negative value. Instead got {gap=}"
            )

        self.sprite_ids: tuple[G, ...] = tuple(grass_objects.keys())
        self.sprite_height: int = tuple(grass_objects.values())[0].get_height()
        self.sprite_width: int = tuple(grass_objects.values())[0].get_width()
        self.sprite_offset: Vector2 = pygame.Vector2(
            self.sprite_width, self.sprite_height
        )

        self.grass_objects: dict[G, dict[int, Surface]] = {
            id: {0: grass_objects[id]} for id in grass_objects
        }
        self.camera_width: int = camera_width + self.sprite_width
        self.camera_height: int = camera_height + self.sprite_height

        self._gap: int = gap
        self._gap_squared: int = self._gap**2
        self._spatial_grid: defaultdict[tuple[int, int], list[Vector2]] = (
            defaultdict(list)
        )
        self._grass_grid: defaultdict[
            tuple[int, int], BinaryGrassTree[GrassSprite[G]]
        ] = defaultdict(BinaryGrassTree)
        self._applied_forces: dict[tuple[int, int], int] = {}

        self.counter: int = 0
        print(self._gap)

    def add_grass(
        self,
        position: Vector2,
        tile_size: tuple[int, int] = (1, 1),
        grass_variants: None | Sequence[G] = None,
    ) -> None:
        """
        adds a blade of grass
        """
        if tile_size != (1, 1):
            step = max(self._gap // 2, 1)
            for x in range(0, tile_size[0] * self._gap, step):
                for y in range(0, tile_size[1] * self._gap, step):
                    vec = pygame.Vector2(position.x + x, position.y + y)
                    self.add_grass(vec)

        spatial_position: tuple[int, int] = self._lock_grid(
            (int(position.x), int(position.y))
        )
        for grid_cell in self._get_boundaries(spatial_position):
            for vector in self._spatial_grid[grid_cell]:
                if (position - vector).length_squared() < self._gap_squared:
                    return

        if grass_variants is None:
            grass_id = random.choice(self.sprite_ids)
        else:
            grass_id = random.choice(grass_variants)

        key = (
            int(position.x // self.camera_width),
            int(position.y // self.camera_height),
        )
        grass = GrassSprite(grass_id, position)

        self._grass_grid[key].insert_node(grass.position.y, grass)
        self._spatial_grid[spatial_position].append(position)
        self.counter += 1

        print(f"PLACED {self.counter} BLADES OF GRASS")

    def get_grass(
        self, camera_pos: Vector2
    ) -> Generator[tuple[Surface, FRect], None, None]:
        """
        returns iterator of all grass from (camera_x, camera_y) to (camera_x + view_width - 1, camera_y + view_width - 1)
        """
        key_x, key_y = (
            int(camera_pos.x // self.camera_width),
            int(camera_pos.y // self.camera_height),
        )
        x_min, x_max = (
            int(camera_pos.x),
            int(camera_pos.x + self.camera_width - 1),
        )
        y_min, y_max = (
            int(camera_pos.y),
            int(camera_pos.y + self.camera_height - 1),
        )

        all_sprites: list[GrassSprite[G]] = []

        for kx in (key_x, key_x + 1):
            for ky in (key_y, key_y + 1):
                for sprite_list in self._grass_grid[
                    (kx, ky)
                ].inorder_traversal():
                    all_sprites.extend(sprite_list)

        return (
            (
                self.grass_objects[sprite.image_id][
                    self._applied_forces.get(
                        (int(sprite.position.x), int(sprite.position.y)), 0
                    )
                ],
                self._cast_rect(
                    "topleft",
                    sprite.position - camera_pos - self.sprite_offset,
                ),
            )
            for sprite in all_sprites
            if x_min <= sprite.position.x <= x_max
            and y_min <= sprite.position.y <= y_max
        )

    def draw(self, surface: Surface, position: Vector2) -> None:
        data = self.get_grass(position)
        surface.blits(data)
        self.clear_force()

    def apply_force(self, position: tuple[int, int], radius_size: int) -> None:
        for point in self._get_circle_points(
            position[0], position[1], radius_size
        ):
            rotation = round((position[0] - point[0]) / 10) * 10
            if rotation < -180:
                rotation = -180
            elif rotation > 180:
                rotation = 180
            # print(rotation)
            self._applied_forces[point] = rotation

            for id in self.grass_objects:
                if self.grass_objects[id].get(rotation) is None:
                    self.grass_objects[id][rotation] = pygame.transform.rotate(
                        self.grass_objects[id][0], rotation
                    )

    def clear_force(self) -> None:
        self._applied_forces.clear()

    def _get_circle_points(
        self, cx: int, cy: int, radius: int
    ) -> Generator[tuple[int, int], None, None]:
        radius2 = radius * radius

        for x in range(cx - radius, cx + radius + 1):
            for y in range(cy - radius, cy + radius + 1):
                dx = x - cx
                dy = y - cy

                if dx * dx + dy * dy <= radius2:
                    yield (x, y)

    def _cast_rect(self, anchor: str, position: Vector2) -> FRect:
        frect = pygame.FRect()
        setattr(frect, anchor, position)
        return frect

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
        # I could've converted this into a loop but hardcoding it gives slightly better performance.
        # Yes. I am micro optimizing. Deal with it.

        x, y = position
        g = self._gap

        # fmt: off
        grid = (
            (x - g, y + g), (x, y + g), (x + g, y + g),
            (x - g, y    ), (x, y    ), (x + g, y    ),
            (x - g, y - g), (x, y - g), (x + g, y - g),
        )
        # fmt: on

        return grid
