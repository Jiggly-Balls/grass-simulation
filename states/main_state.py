from __future__ import annotations

from typing import TYPE_CHECKING

import esper
import pygame
from game_state.utils import StateArgs

from data.constants import WorldEnum
from ecs.processors import BaseProcessor
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

    def process_event(self, event: Event) -> None:
        if event.type == pygame.QUIT:
            self.manager.is_running = False

        elif event.type == pygame.MOUSEWHEEL:
            BaseProcessor.tile_size += event.y * 10
            BaseProcessor.tile_size = max(BaseProcessor.tile_size, 1)

    def process_update(self, dt: float) -> None:
        self.window.fill((50, 50, 50))
        esper.process(dt)
        pygame.display.update()


def hook(**kwargs: Any) -> None:
    MainState.manager.load_states(
        MainState, state_args=[StateArgs(state_name=WorldEnum.MAIN, **kwargs)]
    )
