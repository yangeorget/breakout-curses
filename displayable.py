class Displayable:
    def __init__(self, x: float, y: float, pattern: str):
        self.x = x
        self.y = y
        self.pattern = pattern

    def display(self, window):
        window.addstr(int(self.y), int(self.x), self.pattern)
        window.noutrefresh()

    def erase(self, window):
        window.addstr(int(self.y), int(self.x), " " * len(self.pattern))
        window.noutrefresh()