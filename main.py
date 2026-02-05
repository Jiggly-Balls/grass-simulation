from __future__ import annotations

import pygame
from game_state import StateManager

from data.constants import FPS, SCREEN_RESOLUTION, WorldEnum
from demo import BaseState, MainGame

__version__ = "1.0.0"

pygame.init()
pygame.display.init()
pygame.display.set_caption("Grass Simulation v" + __version__)


def main() -> None:
    window = pygame.display.set_mode(SCREEN_RESOLUTION)
    clock = pygame.time.Clock()

    BaseState.window = window
    BaseState.clock = clock

    manager = StateManager[BaseState](
        bound_state_type=BaseState,
        window=window,
    )
    manager.load_states(MainGame)
    manager.change_state(state_name=WorldEnum.MAIN_GAME)

    assert manager.current_state is not None

    while manager.is_running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            manager.current_state.process_event(event)

        manager.current_state.process_update(dt)


if __name__ == "__main__":
    main()
