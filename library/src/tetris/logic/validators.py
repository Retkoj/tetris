from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tetris.logic.models import Grid


def validate_grid(grid: Grid) -> None:
    width = 10
    height = 20
    if len(grid.cells) != (width * height):
        raise ValueError(f"Grid must consist of {width * height} cells. Current size is {len(grid.cells)}")
