import curses
import queue
import random
import time


class Line(object):
    """Stores a pair of edge positions and can generate an appropriately
    sized string from them"""

    def __init__(self, left, right):
        self.lx self.ly = left
        self.rx self.ry = right

    def __str__(self):
        return " " * (self.rx - self.lx)


class Course(object):
    """Generates and stores a screen's worth of edge positions"""

    def __init__(self):
        self._width, self._height = curses.COLS, curses.LINES
        self._course = queue.deque(maxlen=self._height)
        self._populate()

    def _populate(self):
        for i in range(self._height):
            line = Line(self._gutter)
            self._course.append(line)
            self._new_gutter()

    def evolve(self):
        self._course.popleft()
        self._course.append(Line(self._gutter))  # append something
        return self

    def get_line(self, index):
        return self._course[index]

    def _new_gutter(self):
        direction = random.choice((-1, 0, 1))
        while not 1 < (self._gutter + direction) < self._width:
            direction = random.choice((-1, 0, 1))
        self._gutter += direction

    def __repr__(self):
        return "\n".join(str(line) for line in self._course)

    def __str__(self):
        return "\n".join(str(line) for line in self._course)


class Player(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, ch):
        if ch == curses.KEY_LEFT:
            self.x += -1
        elif ch == curses.KEY_RIGHT:
            self.x += 1

    def is_crashed(self, course):
        player_line = course.get_line(self.y)
        if str(player_line)[self.x] == "!":
            return True
        return False

    def __repr__(self):
        return "X: {} Y: {}".format (self.x, self.y)

    def __str__(self):
        return "H"
        

def main(stdscr):
    curses.curs_set(False)
    stdscr.nodelay(True)
    course = Course()
    start_y = int(curses.LINES / 2)
    start_x = course.get_line(start_y).left_edge + 5
    player = Player(start_x, start_y)

    current_time = time.time()
    while True:
        key_down = stdscr.getch()
        if key_down == ord('q'):
            break
        if not player.is_crashed(course):
            new_time = time.time()
            if new_time - current_time > .1:
                current_time = new_time
                stdscr.addstr(0, 0, str(course.evolve()))
                stdscr.clrtoeol()
            player.update(key_down)
            stdscr.addch(player.y, player.x, str(player))
            stdscr.refresh()
        else:
            stdscr.addstr(player.y, player.x + 1, "<------------ You died here!")
            stdscr.refresh()


if __name__ == '__main__':
    curses.wrapper(main)
