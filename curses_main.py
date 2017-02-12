import curses
import queue
import random
import time


class Line(object):

    EDGE = "!"

    def __init__(self, gutter):
        self._gutter = gutter
        self._generate()

    def _generate(self):
        self._identity = "{gutter}{edge}{middle}{edge}".format(
            gutter=self._gutter * " ",
            edge=self.EDGE,
            middle=" " * 10,
        )

    @property
    def left_edge(self):
        return self._gutter + 1

    def __repr__(self):
        return self._identity

    def __str__(self):
        return self._identity

    def set_player(self, status):
        self._player = status
        self._generate()
        

class Course(object):

    def __init__(self):
        self._width, self._height = curses.COLS, curses.LINES
        self._gutter = 5
        self._course = queue.deque(maxlen=self._height)
        self._populate()

    def _populate(self):
        for i in range(self._height):
            line = Line(self._gutter)
            self._course.append(line)
            self._new_gutter()

    def evolve(self):
        self._course.popleft()                                                   # throw away top line
        self._new_gutter()                                                       # calculate new gutter
        self._course.append(Line(self._gutter))                                  # add new line
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
