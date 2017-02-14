import curses


class Player(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, ch, screen):
        if ch == curses.KEY_LEFT:
            self.x += -1
        elif ch == curses.KEY_RIGHT:
            self.x += 1
        self.send_to_screen(screen)

    def send_to_screen(self, screen):
        screen.addch(self.y, self.x, str(self))

    def is_crashed(self, course):
        player_line = course.get_line(self.y)
        if self.x in (player_line.lx, player_line.rx):
            return True
        return False

    def __repr__(self):
        return "X: {} Y: {}".format (self.x, self.y)

    def __str__(self):
        return "H"
