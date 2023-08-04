import enum
from copy import copy
from dataclasses import dataclass
from functools import cached_property

import numpy as np

from tetris.logic.validators import validate_grid


class TetrisBoardSettings(enum.Enum):
    HEIGHT = 20
    WIDTH = 10
    STARTING_POINT: tuple = (4, 0)


class BlockShapes(enum.Enum):
    T = [(0, 0), (1, 0), (2, 0), (1, 1)]
    Z = [(0, 0), (1, 0), (1, 1), (2, 1)]
    S = [(1, 0), (2, 0), (0, 1), (1, 1)]
    L = [(0, 0), (0, 1), (0, 2), (1, 2)]
    J = [(1, 0), (1, 1), (1, 2), (0, 2)]
    O = [(0, 0), (0, 1), (1, 0), (1, 1)]
    I = [(0, 1), (0, 2), (0, 3), (0, 4)]


class Direction(enum.StrEnum):
    RIGHT = "right"
    LEFT = "left"
    DOWN = "down"
    NO_MOVE = "no move"


@dataclass
class Block:
    block_shape: BlockShapes
    current_location: tuple
    in_motion: bool = True


@dataclass(frozen=True)
class Grid:
    cells: str = ' ' * TetrisBoardSettings.WIDTH.value * TetrisBoardSettings.HEIGHT.value

    # self.start_point = (width - 1) // 2

    def __post_init__(self):
        validate_grid(self)

    @cached_property
    def empty_cell_count(self) -> int:
        return self.cells.count(' ')

    def new_block(self, block: BlockShapes):
        self.place_block(None, self.start_point, block)

    def place_block(self, prev_location, new_location, block: BlockShapes):
        if prev_location is not None:
            zipped = [zip(prev_location, point) for point in block.value]
            old_locations = [tuple([sum(x) for x in d]) for d in zipped]
            for loc in old_locations:
                self.__setitem__(loc, " ")

        zipped = [zip(new_location, point) for point in block.value]
        new_locations = [tuple([sum(x) for x in d]) for d in zipped]
        for loc in new_locations:
            self.__setitem__(loc, "#")

    def print_grid(self):
        for line in self.cells:
            print(line)


@dataclass(frozen=True)
class Move:
    block: Block
    before_state: "GameState"
    after_state: "GameState"


@dataclass(frozen=True)
class GameState:
    grid: Grid

    @cached_property
    def game_over(self) -> bool:
        """game over if blocks get too high"""
        return False

    @cached_property
    def cells_as_matrix(self):
        cell_list = list(self.grid.cells)
        return [cell_list[i: i + TetrisBoardSettings.WIDTH.value]
                for i in range(0, len(cell_list), TetrisBoardSettings.WIDTH.value)]

    def game_not_started(self) -> bool:
        return len(self.grid.cells) == self.grid.empty_cell_count

    def get_random_move(self):
        pass

    def make_move_to(self, direction: Direction, block: Block):
        new_cells = copy(self.cells_as_matrix)

        new_location = block.current_location
        if direction == Direction.RIGHT:
            # TODO dit is niet genoeg check voor rechts
            if (new_location[0] + 1) < TetrisBoardSettings.WIDTH.value:
                new_location = (new_location[0] + 1, new_location[1])
        elif direction == Direction.LEFT:
            if (new_location[0] - 1) >= 0:
                new_location = (new_location[0] - 1, new_location[1])
        elif direction == Direction.DOWN:
            new_location = (new_location[0], new_location[1] + 1)
        # TODO: check valid moves, not just height, also occupied space and left/right
        zipped = [zip(new_location, point) for point in block.block_shape.value]
        new_locations = [tuple([sum(x) for x in d]) for d in zipped]
        in_grid = all([point[1] < TetrisBoardSettings.HEIGHT.value for point in new_locations])

        if in_grid:
            if block.current_location is not None:
                zipped = [zip(block.current_location, point) for point in block.block_shape.value]
                old_locations = [tuple([sum(x) for x in d]) for d in zipped]
                for loc in old_locations:
                    new_cells[loc[1]][loc[0]] = ' '

            for loc in new_locations:
                new_cells[loc[1]][loc[0]] = block.block_shape.name

                block.current_location = new_location
        else:
            block.in_motion = False

        flat_cells = ''.join([item for row in new_cells for item in row])
        return Move(
            block=block,
            before_state=self,
            after_state=GameState(
                grid=Grid(cells=flat_cells)
            )
        )

    def add_new_block(self, block_shape: BlockShapes) -> Move:
        zipped = [zip(TetrisBoardSettings.STARTING_POINT.value, point) for point in block_shape.value]
        new_locations = [tuple([sum(x) for x in d]) for d in zipped]
        new_cells = copy(self.cells_as_matrix)
        for loc in new_locations:
            new_cells[loc[1]][loc[0]] = block_shape.name
        flat_cells = ''.join([item for row in new_cells for item in row])
        block = Block(block_shape=block_shape,
                      current_location=TetrisBoardSettings.STARTING_POINT.value,
                      in_motion=True)
        return Move(
            block=block,
            before_state=self,
            after_state=GameState(
                grid=Grid(cells=flat_cells)
            )
        )

    @cached_property
    def full_rows(self):
        """Returns list of row numbers that don't contain empty places anymore and thus should be removed"""
        # TODO implement block still moving or only check right before new block
        arr = np.array(list(self.grid.cells)).reshape(TetrisBoardSettings.WIDTH.value, TetrisBoardSettings.HEIGHT.value)
        full_rows = []
        for i, row in enumerate(arr):
            if all([" " != v for v in row]):
                full_rows.append(i)
        return full_rows
