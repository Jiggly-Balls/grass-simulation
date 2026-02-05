import time
import random
from typing import Callable, Any

gap = 10


def lock_grid(pos: tuple[int, int]) -> tuple[int, int]:
    return (
        round(pos[0] / gap) * gap,
        round(pos[1] / gap) * gap,
    )


def hard(
    x: int, y: int
) -> tuple[
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
]:
    grid = (
        lock_grid(((x - 1) * gap, (y + 1) * gap)),
        lock_grid(((x) * gap, (y + 1) * gap)),
        lock_grid(((x + 1) * gap, (y + 1) * gap)),
        lock_grid(((x - 1) * gap, (y) * gap)),
        lock_grid(((x + 1) * gap, y * gap)),
        lock_grid(((x - 1) * gap, (y - 1) * gap)),
        lock_grid((x * gap, (y - 1) * gap)),
        lock_grid(((x + 1) * gap, (y - 1) * gap)),
    )
    return grid


def hard2(
    x: int, y: int
) -> tuple[
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
    tuple[int, int],
]:
    # fmt: off
    grid = (
        ((x - 1) * gap, (y + 1) * gap), (x * gap, (y + 1) * gap), ((x + 1) * gap, (y + 1) * gap),
        ((x - 1) * gap, (y    ) * gap), (x      , (y    )      ), ((x + 1) * gap, (y    ) * gap),
        ((x - 1) * gap, (y - 1) * gap), (x * gap, (y - 1) * gap), ((x + 1) * gap, (y - 1) * gap),
    )
    # fmt: on
    return grid


def soft(x: int, y: int) -> list[tuple[int, int]]:
    grid: list[tuple[int, int]] = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                grid.append((x, y))
            else:
                grid.append(((x + dx) * gap, (y + dy) * gap))

    return grid


# h = hard(5, 5)
# h2 = hard2(5, 5)
# s = soft(50, 200)

# pprint(h)
# pprint(h2)
# print()
# pprint(s)

def timeit(loops: int) -> Callable[..., Callable[..., None]]:
    def decor(func: Any) -> Callable[..., None]:
        def wrapper(*args: Any, **kwargs: Any):
            s = time.perf_counter()

            for _ in range(loops):
                func(*args, **kwargs)
            
            print(time.perf_counter() - s)
        return wrapper
    return decor


@timeit(1_000_000)
def hard_test():
    x = random.randint(1, 999_999)
    y = random.randint(1, 999_999)
    hard2(x, y)


@timeit(1_000_000)
def soft_test():
    x = random.randint(1, 999_999)
    y = random.randint(1, 999_999)
    soft(x, y)

hard_test()
print()
soft_test()