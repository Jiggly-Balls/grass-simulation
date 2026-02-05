from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame
from game_state import State
from game_state.utils import MISSING

from core.grass import GrassManager
from core.utils import get_sprite_sheet
from data.constants import GRASS_SPRITE_SHEET, SPRITE_TILE_SIZE, WorldEnum

if TYPE_CHECKING:
    from pygame import Clock, Event, Font, Surface, Vector2


class BaseState(State["BaseState"], ABC):
    window: Surface = MISSING
    clock: Clock = MISSING

    @abstractmethod
    def process_event(self, event: Event) -> None: ...

    @abstractmethod
    def process_update(self, dt: float) -> None: ...


class MainGame(BaseState, state_name=WorldEnum.MAIN_GAME):
    def __init__(self) -> None:
        self.font: Font = pygame.font.SysFont("Arial", 24)
        self.offset: Vector2 = pygame.Vector2()
        self.direction: Vector2 = pygame.Vector2()

        grass_sprites: list[Surface] = get_sprite_sheet(
            path=GRASS_SPRITE_SHEET, tile_size=SPRITE_TILE_SIZE
        )
        grass_id_map: dict[int, Surface] = {
            id: surf for id, surf in enumerate(grass_sprites)
        }
        self.sprite_width: int = grass_sprites[0].get_width()
        self.sprite_height: int = grass_sprites[0].get_height()

        self.grass_manager: GrassManager[int] = GrassManager(grass_id_map)

        self.speed: int = 500
        self.tile_size: int = 3

    def process_event(self, event: Event) -> None:
        if event.type == pygame.QUIT:
            self.manager.is_running = False

        elif event.type == pygame.MOUSEWHEEL:
            self.tile_size += event.y
            self.tile_size = min(max(self.tile_size, 1), 5)

    def process_update(self, dt: float) -> None:
        self.window.fill((50, 50, 50))

        self.handle_add_grass()
        self.grass_manager.draw(self.window, self.offset)
        self.handle_brush()
        self.handle_movement(dt)
        self.handle_fps()

        pygame.display.update()

    def handle_add_grass(self) -> None:
        clicking = pygame.mouse.get_pressed()[0]
        if clicking:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            destination = mouse_pos - self.offset
            destination.x -= self.sprite_width
            destination.y -= self.sprite_height
            self.grass_manager.add(
                destination, (self.tile_size, self.tile_size)
            )

    def handle_brush(self) -> None:
        clicking = pygame.mouse.get_pressed()[0]

        pygame.draw.circle(
            self.window,
            (255, 255, 255),
            pygame.mouse.get_pos(),
            ((self.tile_size / 2) - int(clicking)) * 15,
            2 if not clicking else 0,
        )
        if clicking:
            pygame.draw.circle(
                self.window,
                (255, 255, 255),
                pygame.mouse.get_pos(),
                self.tile_size * 15,
                1,
            )

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

    def handle_fps(self) -> None:
        fps = self.clock.get_fps()
        fps_text = self.font.render(f"FPS: {int(fps)}", False, (255, 255, 255))
        self.window.blit(fps_text, (10, 10))
