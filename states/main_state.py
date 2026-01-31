from __future__ import annotations

from typing import TYPE_CHECKING

import esper
import pygame
from game_state.utils import StateArgs

from data.constants import WorldEnum
from states.base_state import BaseState

if TYPE_CHECKING:
    from typing import Any

    from pygame import Clock, Event, Font, Vector2


class MainState(BaseState, state_name=WorldEnum.MAIN):
    def __init__(self, clock: Clock) -> None:
        self.clock: Clock = clock
        self.font: Font = pygame.font.SysFont("Arial", 24)

        self.offset: Vector2 = pygame.Vector2()
        self.direction: Vector2 = pygame.Vector2()
        self.speed: int = 500
        self.expansion_pad: int = 100

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

        esper.process(self.window, dt)

        # self.handle_movement(dt)
        # self.handle_grass()
        # self.grass_group.draw(self.window, self.offset)

        self.handle_fps()

        pygame.display.update()


def hook(**kwargs: Any) -> None:
    MainState.manager.load_states(
        MainState, state_args=[StateArgs(state_name=WorldEnum.MAIN, **kwargs)]
    )
