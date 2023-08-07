import curses
from curses import wrapper

from game import Game


def main(window):
    game = Game(curses.COLS, curses.LINES)
    game.run(window)


if __name__ == "__main__":
    wrapper(main)
