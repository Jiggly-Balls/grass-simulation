from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Surface


@dataclass(frozen=True)
class Grass:
    image: Surface


@dataclass(frozen=True)
class Transform:
    x: int
    y: int
    rotation: float
