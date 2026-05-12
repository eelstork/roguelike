import curses
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
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
