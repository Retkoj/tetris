from console_renderer import ConsoleRenderer
from players import ConsolePlayer
from tetris.game.engine import Tetris


def main():
    Tetris(ConsolePlayer(), ConsoleRenderer()).play()


if __name__ == '__main__':
    main()
