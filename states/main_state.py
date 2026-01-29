from __future__ import annotations

import random
from typing import TYPE_CHECKING

import pygame
from game_state.utils import StateArgs

from core.grass import GrassGroup, GrassSprite
from core.utils import load_sprite_sheet
from data.constants import GRASS_SPACING, GRASS_SPRITE_SHEET, WorldEnum
from states.base_state import BaseState

if TYPE_CHECKING:
    from typing import Any

    from pygame import Clock, Event, Font, Surface, Vector2


class MainState(BaseState, state_name=WorldEnum.MAIN):
    def __init__(self, clock: Clock) -> None:
        self.clock: Clock = clock
        self.font: Font = pygame.font.SysFont("Arial", 24)

        self.grass_sprites: list[Surface] = load_sprite_sheet(
            GRASS_SPRITE_SHEET
        )
        self.grass_group: GrassGroup = GrassGroup()
        self.grass_vecs: list[Vector2] = []

        self.offset: Vector2 = pygame.Vector2()
        self.direction: Vector2 = pygame.Vector2()
        self.speed: int = 500
        self.expansion_pad: int = 100

    def handle_grass_expansion(self, mouse_pos: Vector2) -> None:
        surf_rect = self.grass_group.grass_surf.get_rect()
        if surf_rect.left > mouse_pos.x or surf_rect.right < mouse_pos.x:
            print("OUTSIDE X")
            dest_x = 0
            width = mouse_pos.x

            if width < 0:
                dest_x = width
                width = abs(width)

            new_surf = pygame.Surface((surf_rect.height, width))
            new_surf.blit(self.grass_group.grass_surf, (dest_x, 0))
            self.grass_group.grass_surf = new_surf

        if surf_rect.top > mouse_pos.y or surf_rect.bottom < mouse_pos.y:
            print("OUTSIDE Y")
            new_surf = ...

    def handle_grass(self) -> None:
        mouse_button_state = pygame.mouse.get_pressed()
        if mouse_button_state[0]:
            mouse_pos = pygame.mouse.get_pos()
            current_vec = pygame.Vector2(*mouse_pos) - self.offset
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
                    self.grass_group.add(
                        GrassSprite(
                            random.choice(self.grass_sprites),
                            brush_vector,
                        )
                    )
                    self.grass_vecs.append(brush_vector)

                    # sorted_sprites = sorted(
                    #     self.grass_group.spritedict.items(),
                    #     key=lambda item: item[0].rect.y,
                    # )
                    # self.grass_group.spritedict = dict(sorted_sprites)

    def handle_grass_new(self) -> None: ...

    def handle_movement(self, dt: float) -> None:
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

        self.offset += self.direction * self.speed * dt
        # print(f"{self.offset}")

    def handle_fps(self) -> None:
        fps = self.clock.get_fps()
        fps_text = self.font.render(f"FPS: {int(fps)}", False, (255, 255, 255))
        self.window.blit(fps_text, (10, 10))

    def process_event(self, event: Event) -> None:
        if event.type == pygame.QUIT:
            self.manager.is_running = False

        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 1:
        #         # print(event.pos)

    def process_update(self, dt: float) -> None:
        self.window.fill((50, 50, 50))

        self.handle_movement(dt)
        self.handle_grass()

        self.grass_group.draw(self.window, self.offset)

        self.handle_fps()

        pygame.display.update()


def hook(**kwargs: Any) -> None:
    MainState.manager.load_states(
        MainState, state_args=[StateArgs(state_name=WorldEnum.MAIN, **kwargs)]
    )
