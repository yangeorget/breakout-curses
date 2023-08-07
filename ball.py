import curses

from brick import BRICK_PATTERN
from paddle import PADDLE_PATTERN
from sprite import Sprite

BALL_PATTERN = "o"
SPEED_RATIO = 40000


class Ball(Sprite):
    def __init__(self, cols, lines):
        super().__init__(cols / 2, lines / 2, BALL_PATTERN)
        self.speed_x = 1 / SPEED_RATIO
        self.speed_y = 1 / SPEED_RATIO

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "speed_x": self.speed_x,
            "speed_y": self.speed_y,
        }

    def move(self, window, game):
        self.erase(window)
        self.x += self.speed_x * len(game.sprites)
        self.y += self.speed_y * len(game.sprites)
        if self.x <= 0:
            self.x = 0
            self.speed_x = -self.speed_x
        if self.x >= curses.COLS - 1:
            self.x = curses.COLS - 1
            self.speed_x = -self.speed_x
        if self.y <= 0:
            self.y = 0
            self.speed_y = -self.speed_y
        if int(self.y) == game.paddle.y and int(self.x) in range(
            game.paddle.x, game.paddle.x + len(PADDLE_PATTERN)
        ):
            half_paddle_length = len(PADDLE_PATTERN) / 2
            self.speed_x = (self.x - (game.paddle.x + half_paddle_length)) / (
                half_paddle_length * SPEED_RATIO
            )
            self.speed_y = -self.speed_y
        elif int(self.y) in range(0, len(game.bricks)):
            brick_x = int(self.x) // len(BRICK_PATTERN)
            brick_y = int(self.y)
            if brick_x in range(0, len(game.bricks[0])):
                brick = game.bricks[brick_y][brick_x]
                if not brick.destroyed:
                    brick.erase(window)
                    brick.destroyed = True
                    self.speed_y = -self.speed_y
        self.display(window)
