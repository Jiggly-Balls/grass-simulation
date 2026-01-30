from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from game_state import State
from game_state.utils import MISSING

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.event import Event

    from ecs.processes import AddGrassProcess, MovementProcess, RenderProcess


class BaseState(State["BaseState"], ABC):
    window: Surface = MISSING
    process_movement: MovementProcess = MISSING
    process_add_grass: AddGrassProcess = MISSING
    process_render: RenderProcess = MISSING

    @abstractmethod
    def process_event(self, event: Event) -> None: ...

    @abstractmethod
    def process_update(self, dt: float) -> None: ...
