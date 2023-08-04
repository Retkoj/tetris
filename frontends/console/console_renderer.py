from typing import Iterable

from tetris.game.renderers import Renderer
from tetris.logic.models import GameState, TetrisBoardSettings


class ConsoleRenderer(Renderer):
    def render(self, game_state: GameState) -> None:
        clear_screen()
        if game_state.full_rows:
            print_blinking_row(game_state.cells_as_matrix, game_state.full_rows)
        else:
            print_solid(game_state.cells_as_matrix)


def clear_screen() -> None:
    print("\033c", end="")


def blink(text: str) -> str:
    return f"\033[5m{text}\033[0m"


def print_blinking_row(cells: Iterable[Iterable[str]], full_rows: Iterable[int]) -> None:
    mutable_cells = list(cells)
    for row in full_rows:
        mutable_cells[row] = blink(mutable_cells[row])
    print_solid(mutable_cells)


def print_solid(cells: Iterable[Iterable[str]]) -> None:
    # TODO: printing is not fast enough in terminal
    width = len(str(max(TetrisBoardSettings.HEIGHT.value, TetrisBoardSettings.WIDTH.value) - 1))

    frame_line = "+-" + "-".join("-" * width for _ in range(TetrisBoardSettings.WIDTH.value)) + "-+\n"

    grid = ''
    grid += frame_line
    grid += "".join(["| " + " ".join(f"{v:{width}s}" for v in row) + " |\n" for row in cells])
    grid += frame_line + '\n'
    print(grid)
