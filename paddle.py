from displayable import Displayable

PADDLE_PATTERN = "_----------_"
PADDLE_SPEED = 2


class Paddle(Displayable):
    def __init__(self, cols, lines):
        super().__init__((cols - len(PADDLE_PATTERN)) // 2, lines - 2, PADDLE_PATTERN)

    def to_dict(self):
        return {"x": self.x, "y": self.y}
