from dataclasses import dataclass
from threading import Timer
from typing import TypeAlias, Callable
from random import choice

from tetris.logic.models import Block, Direction
from tetris.game.players import Player
from tetris.game.renderers import Renderer
from tetris.logic.models import GameState, Grid, BlockShapes

ErrorHandler: TypeAlias = Callable[[Exception], None]


@dataclass(frozen=True)
class Tetris:
    player: Player
    renderer: Renderer
    error_handler: ErrorHandler | None = None

    def play(self):
        game_state = GameState(Grid())
        while True:
            self.renderer.render(game_state)
            block_shape = self.next_block_shape()
            move = game_state.add_new_block(block_shape)
            while move.block.in_motion:
                self.renderer.render(move.after_state)
                timeout = 50
                t = Timer(timeout, self.times_up)
                t.start()
                move = self.player.make_move(move.after_state, move.block)
                t.cancel()
                self.renderer.render(move.after_state)
                move = move.after_state.make_move_to(Direction.DOWN, move.block)
            game_state = move.after_state
            if game_state.game_over:
                break

    @staticmethod
    def next_block_shape() -> BlockShapes:
        return choice(list(BlockShapes))

    @staticmethod
    def times_up():
        pass
