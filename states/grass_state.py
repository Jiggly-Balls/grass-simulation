from __future__ import annotations

import random
from typing import TYPE_CHECKING

import pygame
from game_state import State
from game_state.utils import StateArgs

from core.grass import GrassGroup, GrassSprite
from core.utils import load_sprite_sheet
from data.constants import GRASS_SPACING, GRASS_SPRITE_SHEET

if TYPE_CHECKING:
    from typing import Any

    from pygame import Clock, Event, Font, Surface, Vector2


class GrassState(State):
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

    def handle_grass(self) -> None:
        mouse_button_state = pygame.mouse.get_pressed()
        if mouse_button_state[0]:
            mouse_pos = pygame.mouse.get_pos()
            current_vec = pygame.Vector2(*mouse_pos) - self.offset

            # 3x3 brush
            all_vecs = [current_vec.copy() for _ in range(9)]
            all_vecs[1].x += GRASS_SPACING
            all_vecs[2].x += GRASS_SPACING * 2
            all_vecs[3].y += GRASS_SPACING
            all_vecs[4].x += GRASS_SPACING
            all_vecs[4].y += GRASS_SPACING
            all_vecs[5].x += GRASS_SPACING * 2
            all_vecs[5].y += GRASS_SPACING
            all_vecs[6].y += GRASS_SPACING * 2
            all_vecs[7].x += GRASS_SPACING
            all_vecs[7].y += GRASS_SPACING * 2
            all_vecs[8].x += GRASS_SPACING * 2
            all_vecs[8].y += GRASS_SPACING * 2

            for vec in all_vecs:
                if all(
                    (grass_vec - vec).magnitude() > GRASS_SPACING
                    for grass_vec in self.grass_vecs
                ):
                    print(len(self.grass_group.spritedict))
                    self.grass_group.add(
                        GrassSprite(
                            self.grass_group,
                            random.choice(self.grass_sprites),
                            vec,
                        )
                    )
                    self.grass_vecs.append(vec)

                    sorted_sprites = sorted(
                        self.grass_group.spritedict.items(),
                        key=lambda item: item[0].rect.y,
                    )
                    self.grass_group.spritedict = dict(sorted_sprites)

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

    def process_update(self, *args: Any) -> None:
        self.window.fill((50, 50, 50))

        self.handle_movement(args[0])
        self.handle_grass()

        self.grass_group.draw(self.window, self.offset)

        self.handle_fps()

        pygame.display.update()


def hook(**kwargs: Any) -> None:
    GrassState.manager.load_states(
        GrassState, state_args=[StateArgs(state_name="GrassState", **kwargs)]
    )
