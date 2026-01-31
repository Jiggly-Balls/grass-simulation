from __future__ import annotations

import esper
import pygame
from game_state import StateManager

from data.constants import FPS, SCREEN_RESOLUTION, WorldEnum
from ecs.processors import BaseProcessor
from states.base_state import BaseState

__version__ = "0.1.0"

pygame.init()
pygame.display.init()
pygame.display.set_caption("Gass Simulation v" + __version__)


def main() -> None:
    window = pygame.display.set_mode(SCREEN_RESOLUTION)
    clock = pygame.time.Clock()

    manager = StateManager[BaseState](
        bound_state_type=BaseState,
        window=window,
    )
    manager.connect_state_hook("states.main_state", clock=clock)
    manager.change_state(state_name=WorldEnum.MAIN)

    esper.switch_world(WorldEnum.MAIN)
    for processor in BaseProcessor.cls_processors:
        esper.add_processor(processor_instance=processor())

    assert manager.current_state is not None

    while manager.is_running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            manager.current_state.process_event(event)

        manager.current_state.process_update(dt)


if __name__ == "__main__":
    main()
