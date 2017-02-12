import curses
import queue
import random
import time


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


class Course(object):
    """Generates and stores a screen's worth of edge positions"""

    MIN_WIDTH = 6
    MAX_WIDTH = 25

    def __init__(self):
        self._width, self._height = curses.COLS - 1 , curses.LINES - 1
        self._course = queue.deque(maxlen=self._height)
        self._left_edge = 5
        self._right_edge = 15
        self._populate()

    def _populate(self):
        for i in range(self._height):
            line = Line(self._left_edge, self._right_edge)
            self._course.append(line)
            self._update_edges()
            self._update_lines()

    def evolve(self):
        self._course.popleft()
        self._update_edges()
        self._update_lines()
        self._course.append(Line(self._left_edge, self._right_edge))

    def _update_lines(self):
        [l.update() for l in self._course]

    @property
    def lines(self):
        return self._course

    def get_line(self, index):
        return self._course[index]

    def _update_edges(self):
        left_choices = {
            self.MIN_WIDTH: (-1, 0),
            self.MAX_WIDTH: (0, 1)
        }
        right_choices = {
            self.MIN_WIDTH: (0, 1),
            self.MAX_WIDTH: (-1, 0)
        }
        current_distance = self._right_edge - self._left_edge
        choices = left_choices.get(current_distance, (-1, 0, 1))
        direction = random.choice(choices)
        while not self._left_edge + direction > 1:
            direction = random.choice(choices)
        self._left_edge += direction

        current_distance = self._right_edge - self._left_edge
        choices = right_choices.get(current_distance, (-1, 0, 1))
        direction = random.choice(choices)
        while not self._right_edge + direction < self._width:
            direction = random.choice(choices)
        self._right_edge += direction


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
        if self.x in (player_line.lx, player_line.rx):
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
    start_x = course.get_line(start_y).lx + 5
    player = Player(start_x, start_y)
    distance = 0

    current_time = time.time()
    while True:
        key_down = stdscr.getch()
        if key_down == ord('q'):
            break
        if not player.is_crashed(course):
            new_time = time.time()
            if new_time - current_time > .1:
                distance += 1
                current_time = new_time
                course.evolve()
                stdscr.clear()
                [stdscr.addstr(line.y, line.lx, str(line)) for line in course.lines]
            player.update(key_down)
            stdscr.addch(player.y, player.x, str(player))
            stdscr.refresh()
        else:
            stdscr.addstr(player.y, player.x + 1, "<------------ You died here! But you made it {} feet!".format(distance))
            stdscr.refresh()


if __name__ == '__main__':
    curses.wrapper(main)
