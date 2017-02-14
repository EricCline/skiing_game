import curses
import queue
import random

from ski import Line


class Course(object):
    """Generates and stores a screen's worth of edge positions"""

    MIN_WIDTH = 6
    MAX_WIDTH = 25

    def __init__(self, height, width):
        self._height, self._width = height, width
        self._course = queue.deque(maxlen=self._height)
        self._left_edge = 10
        self._right_edge = self._left_edge + self.MAX_WIDTH
        self._populate()

    def _populate(self):
        for i in range(self._height):
            self._course.append(
                Line(self._left_edge, self._right_edge)
            )
            self._update_lines()
            if i > self._height / 1.25:
                self._update_edges()

    def update(self, screen):
        self._course.popleft()
        self._update_edges()
        self._update_lines()
        self._course.append(Line(self._left_edge, self._right_edge))
        self.send_to_screen(screen)

    def send_to_screen(self, screen):
        screen.clear()
        [
            screen.addstr(y, line.lx, str(line))
            for y, line in enumerate(self._course)
        ]

    def _update_lines(self):
        [l.update() for l in self._course]

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
