from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from game_state.utils import MISSING

if TYPE_CHECKING:
    from pygame import Surface, Vector2


@dataclass(slots=True)
class Renderable:
    image: Surface
    width: int = MISSING
    height: int = MISSING

    def __post_init__(self) -> None:
        if self.width is MISSING:
            self.width = self.image.get_width()
        if self.height is MISSING:
            self.height = self.image.get_height()


@dataclass(slots=True)
class Transform:
    rotation: float = 0.0
    position: Vector2 = MISSING

    def __post_init__(self) -> None:
        if self.position is MISSING:
            self.position = Vector2()
