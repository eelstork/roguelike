import curses
import _curses
from roguelike.engine import Game

def main():
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

if __name__ == '__main__':
    main()
