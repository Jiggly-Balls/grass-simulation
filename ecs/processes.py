from __future__ import annotations

import random
from typing import TYPE_CHECKING, final

import esper
import pygame
from esper import Processor

from core.utils import load_sprite_sheet
from data.constants import (
    GRASS_SPACING,
    GRASS_SPRITE_SHEET,
    SPEED,
    ProcessorPriority,
)
from ecs.components import Renderable, Transform

if TYPE_CHECKING:
    from pygame import Surface, Vector2


@final
class MovementProcess(Processor):
    priority: int = int(ProcessorPriority.MOVEMENT)
    offset: Vector2 = Vector2()

    def __init__(self) -> None:
        self.direction: Vector2 = pygame.Vector2()

    def update(self, dt: float) -> None:
        key_pressed = pygame.key.get_pressed()

        # for _, (_, transform) in esper.get_components(Renderable, Transform):

        if key_pressed[pygame.K_w]:
            self.direction.y = 1
        elif key_pressed[pygame.K_s]:
            self.direction.y = -1
        else:
            self.direction.y = 0

        if key_pressed[pygame.K_d]:
            self.direction.x = -1
        elif key_pressed[pygame.K_a]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if self.direction.magnitude() != 0.0:
            self.direction.normalize_ip()

        MovementProcess.offset += self.direction * SPEED * dt


@final
class AddGrassProcess(Processor):
    priority: int = int(ProcessorPriority.ADD_GRASS)
    grass_sprites: list[Surface] = load_sprite_sheet(GRASS_SPRITE_SHEET)

    def __init__(self) -> None:
        self.grass_vecs: list[Vector2] = []

    def update(self) -> None:
        mouse_button_state = pygame.mouse.get_pressed()
        if mouse_button_state[0]:
            mouse_pos = pygame.mouse.get_pos()
            current_vec = pygame.Vector2(*mouse_pos) - MovementProcess.offset
            # self.handle_grass_expansion(current_vec)

            # 3x3 brush
            brush_vectors = [current_vec.copy() for _ in range(9)]
            brush_vectors[1].x += GRASS_SPACING
            brush_vectors[2].x += GRASS_SPACING * 2
            brush_vectors[3].y += GRASS_SPACING
            brush_vectors[4].x += GRASS_SPACING
            brush_vectors[4].y += GRASS_SPACING
            brush_vectors[5].x += GRASS_SPACING * 2
            brush_vectors[5].y += GRASS_SPACING
            brush_vectors[6].y += GRASS_SPACING * 2
            brush_vectors[7].x += GRASS_SPACING
            brush_vectors[7].y += GRASS_SPACING * 2
            brush_vectors[8].x += GRASS_SPACING * 2
            brush_vectors[8].y += GRASS_SPACING * 2

            for brush_vector in brush_vectors:
                if all(
                    (grass_vec - brush_vector).magnitude() > GRASS_SPACING
                    for grass_vec in self.grass_vecs
                ):
                    # print(len(self.grass_group.grass_objects))
                    # self.grass_group.add(
                    #     GrassSprite(
                    #         random.choice(self.grass_sprites),
                    #         brush_vector,
                    #     )
                    # )

                    self.grass_vecs.append(brush_vector)

                    esper.create_entity(
                        Renderable(image=random.choice(self.grass_sprites)),
                        Transform(position=brush_vector),
                    )

                    # sorted_sprites = sorted(
                    #     self.grass_group.spritedict.items(),
                    #     key=lambda item: item[0].rect.y,
                    # )
                    # self.grass_group.spritedict = dict(sorted_sprites)


class RenderProcess(Processor):
    priority: int = int(ProcessorPriority.RENDER)

    def update(self) -> None: ...
