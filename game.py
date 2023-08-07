import curses
from curses import curs_set
from typing import List

from ammo import Ammo
from ball import Ball
from brick import Brick, BRICK_PATTERN
from paddle import Paddle, PADDLE_SPEED, PADDLE_PATTERN
from sprite import Sprite


KEY_SPACE = 32
GUN_POWER_MAX = 5

class Game:
    def __init__(self, cols: int, lines: int):
        self.cols = cols
        self.lines = lines
        self.bricks = [
            [
                Brick(x * len(BRICK_PATTERN), y)
                for x in range(0, cols // len(BRICK_PATTERN))
            ]
            for y in range(0, lines // 4)
        ]
        self.ball = Ball(cols, lines)
        self.paddle = Paddle(cols, lines)
        self.sprites: List[Sprite] = [self.ball]
        self.gun_power = GUN_POWER_MAX

    def debug(self, window):
        window.addstr(0, 0, str(self.paddle.to_dict()))
        window.addstr(1, 0, str(self.ball.to_dict()))

    def run(self, window):
        curs_set(False)  # do not blink
        window.nodelay(True)  # no blocking input
        window.clear()
        for sprite in self.sprites:
            sprite.display(window)
        self.paddle.display(window)
        for y in range(0, len(self.bricks)):
            for x in range(0, len(self.bricks[y])):
                self.bricks[y][x].display(window)
        curses.doupdate()
        while not (self.won() or self.lost()):
            self.gun_power += 1
            if self.gun_power >= GUN_POWER_MAX:
                self.gun_power = GUN_POWER_MAX
            key = window.getch()
            if key == KEY_SPACE and self.gun_power == GUN_POWER_MAX:
                self.sprites.append(Ammo(self.paddle))
                self.gun_power = 0
            if key == curses.KEY_LEFT:
                self.paddle.erase(window)
                self.paddle.x = max(self.paddle.x - PADDLE_SPEED, 0)
            if key == curses.KEY_RIGHT:
                self.paddle.erase(window)
                self.paddle.x = min(
                    self.paddle.x + PADDLE_SPEED, curses.COLS - len(PADDLE_PATTERN)
                )
            self.paddle.display(window)
            for sprite in self.sprites:
                sprite.move(window, self)
            self.sprites = [sprite for sprite in self.sprites if not sprite.destroyed]
            curses.doupdate()
        if self.lost():
            window.addstr(self.lines // 2, self.cols // 2, "GAME OVER")
        else:
            window.addstr(self.lines // 2, self.cols // 2, "YOU WON")
        window.nodelay(False)
        window.getch()

    def won(self):
        for brick_line in self.bricks:
            for brick in brick_line:
                if not brick.destroyed:
                    return False
        return True

    def lost(self):
        return int(self.ball.y) > self.paddle.y
