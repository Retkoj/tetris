import abc
import time

from tetris.logic.models import Block
from tetris.logic.exceptions import InvalidMove
from tetris.logic.models import GameState, Move


class Player(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        pass

    def make_move(self, game_state: GameState, block: Block) -> Move:
        if move := self.get_move(game_state, block):
            return move
        raise InvalidMove("No more possible moves")

    @abc.abstractmethod
    def get_move(self, game_state: GameState, block: Block) -> Move | None:
        """Return the current player's move in the given game state"""


class ComputerPlayer(Player, metaclass=abc.ABCMeta):
    def __init__(self, delay_seconds: float = 0.25) -> None:
        super().__init__()
        self.delay_seconds = delay_seconds

    def get_move(self, game_state: GameState) -> Move | None:
        time.sleep(self.delay_seconds)
        return self.get_computer_move(game_state)

    @abc.abstractmethod
    def get_computer_move(self, game_state: GameState) -> Move | None:
        """Return computer's move"""


class RandomComputerPlayer(ComputerPlayer):
    """Picks moves at random from all possible moves in a game state"""
    def get_computer_move(self, game_state: GameState) -> Move | None:
        return game_state.get_random_move()
