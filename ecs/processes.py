from typing import final

from esper import Processor

from data.constants import ProcessorPriority


@final
class MovementProcess(Processor):
    priority: int = int(ProcessorPriority.MOVEMENT)

    def update(self) -> None: ...
