from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from game_state import State

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.event import Event


class BaseState(State["BaseState"], ABC):
    window: Surface

    @abstractmethod
    def process_event(self, event: Event) -> None: ...

    @abstractmethod
    def process_update(self, dt: float) -> None: ...
