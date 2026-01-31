from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, final

import esper
import pygame
from esper import Processor
from game_state.utils import MISSING

from core.utils import get_sprite_sheet
from data.constants import (
    GRASS_ABUNDANCE,
    GRASS_SPACING,
    GRASS_SPRITE_SHEET,
    SPEED,
    ProcessorPriority,
)
from ecs.components import Renderable, Transform

if TYPE_CHECKING:
    from pygame import Surface, Vector2
    from pygame.font import Font
    from pygame.time import Clock


class BaseProcessor(Processor, ABC):
    cls_processors: list[type[BaseProcessor]] = []

    tile_size: int = 32

    window: Surface = MISSING
    clock: Clock = MISSING

    def __init_subclass__(cls) -> None:
        BaseProcessor.cls_processors.append(cls)

    @abstractmethod
    def process(self, dt: float) -> None: ...


@final
class MovementProcess(BaseProcessor):
    priority: int = int(ProcessorPriority.MOVEMENT)
    offset: Vector2 = pygame.Vector2()

    def __init__(self) -> None:
        self.direction: Vector2 = pygame.Vector2()

    def process(self, dt: float) -> None:
        key_pressed = pygame.key.get_pressed()

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
class AddGrassProcess(BaseProcessor):
    priority: int = int(ProcessorPriority.ADD_GRASS)

    def __init__(self) -> None:
        self.grass_vecs: list[Vector2] = []
        self.grass = 0

    def process(self, dt: float) -> None:
        mouse_button_state = pygame.mouse.get_pressed()
        if mouse_button_state[0]:
            mouse_pos = pygame.mouse.get_pos()
            current_vec = pygame.Vector2(*mouse_pos) - MovementProcess.offset
            # self.handle_grass_expansion(current_vec)

            brush_vectors: list[Vector2] = [current_vec]
            for _ in range(GRASS_ABUNDANCE - 1):
                x_start = int(current_vec.x - current_vec.x % self.tile_size)
                y_start = int(current_vec.y - current_vec.y % self.tile_size)

                x_pos = (
                    random.randint(x_start, x_start + self.tile_size)
                    - self.tile_size // 2
                )
                y_pos = (
                    random.randint(y_start, y_start + self.tile_size)
                    - self.tile_size // 2
                )

                new_grass = pygame.Vector2(x_pos, y_pos)
                brush_vectors.append(new_grass)

            for brush_vector in brush_vectors:
                if all(
                    (grass_vec - brush_vector).magnitude() > GRASS_SPACING
                    for grass_vec in self.grass_vecs
                ):
                    self.grass_vecs.append(brush_vector)

                    esper.create_entity(
                        Renderable(
                            image=random.choice(
                                get_sprite_sheet(GRASS_SPRITE_SHEET)
                            )
                        ),
                        Transform(position=brush_vector),
                    )
                    self.grass += 1
                    print(f"CREATED {self.grass} GRASS BLADES")

                    # sorted_sprites = sorted(
                    #     self.grass_group.spritedict.items(),
                    #     key=lambda item: item[0].rect.y,
                    # )
                    # self.grass_group.spritedict = dict(sorted_sprites)


class RenderProcess(BaseProcessor):
    priority: int = int(ProcessorPriority.RENDER)

    def process(self, dt: float) -> None:
        blit_data: list[tuple[Surface, Vector2]] = []
        for _, (renderable, transform) in esper.get_components(
            Renderable, Transform
        ):
            blit_data.append(
                (renderable.image, transform.position + MovementProcess.offset)
            )

            # self.window.blit(
            #     renderable.image, transform.position + MovementProcess.offset
            # )

        clicking = pygame.mouse.get_pressed()[0]

        self.window.blits(blit_data)
        pygame.draw.circle(
            self.window,
            (255, 255, 255),
            pygame.mouse.get_pos(),
            (self.tile_size / 2) - int(clicking) * 2,
            2 if not clicking else 0,
        )
        if clicking:
            pygame.draw.circle(
                self.window,
                (255, 255, 255),
                pygame.mouse.get_pos(),
                self.tile_size,
                1,
            )


class FPSHandleProcessor(BaseProcessor):
    priority: int = int(ProcessorPriority.FPS_HANDLE)

    def __init__(self) -> None:
        self.font: Font = pygame.font.SysFont("Arial", 24)

    def process(self, dt: float) -> None:
        fps = self.clock.get_fps()
        fps_text = self.font.render(f"FPS: {int(fps)}", False, (255, 255, 255))
        self.window.blit(fps_text, (10, 10))
