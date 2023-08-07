from displayable import Displayable

BRICK_PATTERN = "[------]"


class Brick(Displayable):
    def __init__(self, x, y):
        super().__init__(x, y, BRICK_PATTERN)
        self.destroyed = False
