import curses
import os
import queue
import random
import time



class Line(object):

    EDGE = "!"

    def __init__(self, gutter, player=False):
        self._gutter = gutter
        self._player = player
        self._generate()

    def _generate(self):
        self._identity = "{gutter}{edge}{left_margin}{player}{right_margin}{edge}".format(
            gutter=self._gutter * " ",
            edge=self.EDGE,
            left_margin=" " * 5,
            player = "H" if self._player else " ",
            right_margin=" " * 5,
        )

    def __repr__(self):
        return self._identity

    def __str__(self):
        return self._identity

    def set_player(self, status):
        self._player = status
        self._generate()
        

class Screen(object):

    def __init__(self):
        self._width, self._height = os.get_terminal_size()
        self._gutter = 5
        self._screen = queue.deque(maxlen=self._height)
        self._player_index = int(self._height / 2)  # put the player in the middle
        self._populate()

    def _populate(self):
        for i in range(self._height):
            if i == self._player_index:
                line = Line(self._gutter, player=True)
            else:
                line = Line(self._gutter)
            self._screen.append(line)
            self._new_gutter()

    def evolve(self, direction):
        self._screen[self._player_index].set_player(False)                       # remove player
        self._screen.popleft()                                                   # throw away top line
        self._screen[self._player_index].set_player(True)                        # add player
        self._new_gutter()                                                       # calculate new gutter
        self._screen.append(Line(self._gutter))                                  # add new line
        return self

    def _new_gutter(self):
        direction = random.choice((-1, 0, 1))
        while not 1 < (self._gutter + direction) < self._width:
            direction = random.choice((-1, 0, 1))
        self._gutter += direction

    def __repr__(self):
        return "\n".join(str(line) for line in self._screen)


def get_user_input():
    """
    Use sys.stdin to get the user's input for moving the skier.
    assist from: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/134892
    added the select for non-blocking to the above recipe
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        inputflag, _, _ = select.select([fd], [], [], 0.1)
        if len(inputflag) == 1:
            userinput = sys.stdin.read(3)
        else:
            userinput = None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return userinput


def loop():
    screen = Screen()

    while True:
        time.sleep(.1)
#        user_input = get_user_input()
#        if user_input == '\x1b[C':
#            print("right")
#            direction = 1 
#        elif user_input == '\x1b[D':
#            direction = -1
#        else:
#            direction = 0
#        print(screen.evolve(direction))
        print(screen.evolve(0))


#if __name__ == '__main__':
#    loop()

def main(stdscr):
    passs



if __name__ == '__main__':
    curses.wrapper(main)
