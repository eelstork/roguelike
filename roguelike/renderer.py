import argparse
import curses
import _curses
from roguelike.engine import Game

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=20)
    parser.add_argument('--height', type=int, default=20)
    args = parser.parse_args()

    game = Game(args.width, args.height)
    
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
            elif key == curses.KEY_UP or key == ord('k'):
                action = 'up'
            elif key == curses.KEY_DOWN or key == ord('j'):
                action = 'down'
            elif key == curses.KEY_LEFT or key == ord('h'):
                action = 'left'
            elif key == curses.KEY_RIGHT or key == ord('l'):
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
