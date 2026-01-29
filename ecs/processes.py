from __future__ import annotations

from typing import TYPE_CHECKING, final

import esper
import pygame
from esper import Processor

from data.constants import SPEED, ProcessorPriority
from ecs.components import Renderable, Transform

if TYPE_CHECKING:
    from pygame import Vector2


@final
class MovementProcess(Processor):
    priority: int = int(ProcessorPriority.MOVEMENT)

    def __init__(self) -> None:
        self.direction: Vector2 = pygame.Vector2()

    def update(self, dt: float) -> None:
        key_pressed = pygame.key.get_pressed()

        for _, (_, transform) in esper.get_components(Renderable, Transform):
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

            transform.offset += self.direction * SPEED * dt
            # print(f"{self.offset}")
