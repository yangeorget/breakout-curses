from displayable import Displayable


class Sprite(Displayable):
    def __init__(self, x: float, y: float, pattern: str):
        self.x = x
        self.y = y
        self.pattern = pattern
        self.destroyed = False

    def move(self, window):
        pass
