import curses
import _curses
import sys
from roguelike.engine import Game

class RoguelikeEnv:
    def __init__(self, width=20, height=20):
        self.game = Game(width, height)

    def step(self, action):
        self.game.step(action)
        return self.game.render(), self.game.done

    def render(self):
        return self.game.render()

    @property
    def done(self):
        return self.game.done

def run_curses():
    game = Game(20, 20)
    
    def run(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(False)
        stdscr.keypad(True)
        
        while not game.done:
            stdscr.clear()
            stdscr.addstr(game.render())
            stdscr.refresh()
            
            key = stdscr.getch()
            action = None
            
            if key == ord('q'):
                action = 'quit'
            elif key == curses.KEY_UP or key == ord('w'):
                action = 'up'
            elif key == curses.KEY_DOWN or key == ord('s'):
                action = 'down'
            elif key == curses.KEY_LEFT or key == ord('a'):
                action = 'left'
            elif key == curses.KEY_RIGHT or key == ord('d'):
                action = 'right'
            
            if action:
                game.step(action)
                
    try:
        curses.wrapper(run)
    except (_curses.error, curses.error):
        print("Error: Could not initialize curses. Make sure you are running this in a terminal.")
    except KeyboardInterrupt:
        pass

def main():
    if sys.stdin.isatty():
        run_curses()
    else:
        # Machine agent mode: simple loop or importable interface
        # For this exercise, maybe just print to stdout for now
        # but the request asks to make it playable by agents.
        # Allowing an import of RoguelikeEnv is the key.
        pass

if __name__ == '__main__':
    main()
