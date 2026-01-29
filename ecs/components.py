from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from game_state.utils import MISSING

if TYPE_CHECKING:
    from pygame import Surface


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
    x: int
    y: int
    rotation: float
