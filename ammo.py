from brick import BRICK_PATTERN
from paddle import PADDLE_PATTERN
from sprite import Sprite

AMMO_PATTERN = "|"
SPEED_RATIO = 5000


class Ammo(Sprite):
    def __init__(self, paddle):
        super().__init__(paddle.x + len(PADDLE_PATTERN) / 2, paddle.y - 1, AMMO_PATTERN)
        self.speed_y = -1 / SPEED_RATIO

    def to_dict(self):
        return {"x": self.x, "y": self.y, "speed_y": self.speed_y}

    def move(self, window, game):
        self.erase(window)
        self.y += self.speed_y * len(game.sprites)
        if self.y <= 0:
            self.y = 0
            self.destroyed = True
        if int(self.y) in range(0, len(game.bricks)):
            brick_x = int(self.x) // len(BRICK_PATTERN)
            brick_y = int(self.y)
            if brick_x in range(0, len(game.bricks[brick_y])):
                brick = game.bricks[brick_y][brick_x]
                if not brick.destroyed:
                    self.destroyed = True
                    brick.erase(window)
                    brick.destroyed = True
        if not self.destroyed:
            self.display(window)
