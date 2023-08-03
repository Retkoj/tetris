import argparse

from players import ConsolePlayer

PLAYER_CLASSES = {
    "human": ConsolePlayer
}


def parse_args():
    parser = argparse.ArgumentParser(prog="Tetris", description="Tetris game")

    return parser.parse_args()
