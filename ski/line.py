import curses


class Line(object):
    """Stores a pair of edge positions and can generate an appropriately
    sized string from them"""

    EDGE = "!"

    def __init__(self, left, right):
        self.lx = left
        self.rx = right
        self.y = curses.LINES - 1

    def update(self):
        self.y += -1

    def __str__(self):
        return "{edge}{middle}{edge}".format(edge=self.EDGE, middle=" " * (self.rx - self.lx))
