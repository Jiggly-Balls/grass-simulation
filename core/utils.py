from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Any

import pygame

if TYPE_CHECKING:
    from collections.abc import Generator

    from pygame import Surface

__all__ = ("get_sprite_sheet",)


@functools.cache
def get_sprite_sheet(path: str, tile_size: int) -> list[Surface]:
    sprite_sheet = pygame.image.load(path).convert()
    total_frames = sprite_sheet.get_size()[0] // tile_size
    images: list[Surface] = []

    for offset in range(total_frames):
        surf = pygame.Surface((tile_size, tile_size)).convert()
        total_offset = offset * tile_size
        surf.blit(
            sprite_sheet,
            area=(
                0 + total_offset,
                0,
                tile_size + total_offset,
                tile_size + total_offset,
            ),
        )
        surf.set_colorkey((0, 0, 0))
        width, height = surf.get_size()

        expanded_surf = pygame.transform.scale(
            surf, (width * 1.5, height * 1.5)
        )
        images.append(expanded_surf)

    return images


class GrassNode[N]:
    def __init__(self, lead: int, *data: N) -> None:
        self.lead: int = lead
        self.data: list[N] = list(data)

        self.left: None | GrassNode[N] = None
        self.right: None | GrassNode[N] = None

    def __repr__(self) -> str:
        return f"TreeNode(lead={self.lead} | elements={len(self.data)})"


class BinaryGrassTree[N]:
    def __init__(self) -> None:
        self.root: None | GrassNode[N] = None

    def insert_node(self, lead: int, *data: N) -> None:
        if self.root is None:
            self.root = GrassNode(lead, *data)
        else:
            self._recursive_insert(self.root, lead, *data)

    def inorder_traversal(self) -> Generator[list[N], Any, None]:
        yield from self._recursive_inorder(self.root)

    def _recursive_inorder(
        self, node: None | GrassNode[N]
    ) -> Generator[list[N], Any, None]:
        if node is not None:
            yield from self._recursive_inorder(node.left)
            yield node.data
            yield from self._recursive_inorder(node.right)

    def _recursive_insert(
        self, node: GrassNode[N], lead: int, *data: N
    ) -> None:
        if lead == node.lead:
            node.data.extend(data)

        elif lead < node.lead:
            if node.left is None:
                node.left = GrassNode(lead, *data)
            else:
                self._recursive_insert(node.left, lead, *data)

        else:
            if node.right is None:
                node.right = GrassNode(lead, *data)
            else:
                self._recursive_insert(node.right, lead, *data)


if __name__ == "__main__":
    tree = BinaryGrassTree[int]()
    tree.insert_node(5, 55)
    tree.insert_node(4, 44)
    tree.insert_node(3, 33)
    tree.insert_node(2, 22)
    tree.insert_node(9, 99)
    tree.insert_node(7, 77)
    print(tree.root)
    print()
    for i in tree.inorder_traversal():
        print(i)
