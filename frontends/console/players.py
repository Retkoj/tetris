from pynput import keyboard
from pynput.keyboard import Key

from tetris.logic.models import Block
from tetris.game.players import Player
from tetris.logic.models import GameState, Move, Direction


class ConsolePlayer(Player):
    def __init__(self):
        super().__init__()
        self.listener = keyboard.Listener(
            on_release=self.on_key_release)
        self.listener.start()
        self.direction = Direction.NO_MOVE

    def on_key_release(self, key):
        if key == Key.right:
            self.direction = Direction.RIGHT
        elif key == Key.left:
            self.direction = Direction.LEFT
        elif key == Key.down:
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.NO_MOVE

    def get_move(self, game_state: GameState, block: Block) -> Move | None:
        while not game_state.game_over:
            move = game_state.make_move_to(self.direction, block)
            self.direction = Direction.NO_MOVE
            return move
        return None
