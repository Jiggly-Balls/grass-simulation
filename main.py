import pygame
from game_state import StateManager

from data.constants import FPS, SCREEN_RESOLUTION
from states.base_state import BaseState

__version__ = "0.1.0"

pygame.init()
pygame.display.init()
pygame.display.set_caption("Gass Simulation v" + __version__)


def main() -> None:
    window = pygame.display.set_mode(SCREEN_RESOLUTION)
    clock = pygame.time.Clock()

    manager = StateManager[BaseState](
        window=window, bound_state_type=BaseState
    )
    manager.connect_state_hook("states.grass_state", clock=clock)
    manager.change_state("GrassState")

    assert manager.current_state is not None

    while manager.is_running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            manager.current_state.process_event(event)

        manager.current_state.process_update(dt)


if __name__ == "__main__":
    main()
