import curses
import time

from ski import Course, Player


class Game(object):

    def __init__(self, screen):
        curses.curs_set(False)
        self.screen = screen
        height, width = curses.LINES - 1, curses.COLS - 1
        self.course = Course(height, width)
        self.player = Player(*self.starting_coordinates())

    def starting_coordinates(self):
        start_y = int(curses.LINES / 2)
        player_line = self.course.get_line(start_y)
        width = player_line.rx - player_line.lx
        start_x = player_line.lx + int(width / 2)
        return start_x, start_y

    def add_ready(self):
        y = self.player.y - 2
        msg = "Press any key to begin!"
        self.screen.addstr(y, self.player.x - int(len(msg) / 2), msg)
        self.screen.refresh()
        self.screen.getch()

    def play(self):
        distance = 0
        current_time = time.time()
        self.course.send_to_screen(self.screen)
        self.player.send_to_screen(self.screen)
        self.screen.refresh()
        self.add_ready()
        self.screen.nodelay(True)
        while True:
            key_down = self.screen.getch()
            if key_down == ord('q'):
                break
            if not self.player.is_crashed(self.course):
                self.player.update(key_down, self.screen)
                new_time = time.time()
                if new_time - current_time > .1:
                    distance += 1
                    current_time = new_time
                    self.course.update(self.screen)
                self.screen.refresh()
            else:
                self.screen.addstr(
                    self.player.y,
                    self.player.x + 1,
                    "<------------ You died here! But you made it {} feet!".format(distance))
                self.screen.refresh()
