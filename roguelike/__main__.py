import argparse
import json
import os
import sys
# The parent directory is already in PYTHONPATH when running `python -m roguelike`
# So we don't strictly need to modify sys.path if invoked correctly.
from roguelike.engine import Game

def save_game(game, path):
    data = {
        'width': game.width,
        'height': game.height,
        'player_pos': list(game.player_pos),
        'done': game.done
    }
    with open(path, 'w') as f:
        json.dump(data, f)

def load_game(path):
    with open(path, 'r') as f:
        data = json.load(f)
    game = Game(data['width'], data['height'])
    game._player_pos = data['player_pos']
    game._done = data['done']
    return game

def handle_step(args):
    path = args.state
    if os.path.exists(path):
        game = load_game(path)
    else:
        game = Game()
    
    if args.action not in ['up', 'down', 'left', 'right', 'quit']:
        # print to stderr so it doesn't pollute stdout for the machine agent
        print(f"Invalid action: {args.action}", file=sys.stderr)
        sys.exit(1)
        
    game.step(args.action)
    save_game(game, path)
    print(game.render())

def handle_show(args):
    path = args.state
    if os.path.exists(path):
        game = load_game(path)
    else:
        game = Game()
    print(game.render())

def main():
    parser = argparse.ArgumentParser(prog='roguelike')
    subparsers = parser.add_subparsers()

    play_parser = subparsers.add_parser('play')
    play_parser.set_defaults(func=run_interactive)

    step_parser = subparsers.add_parser('step')
    step_parser.add_argument('action')
    step_parser.add_argument('--state', required=True)
    step_parser.set_defaults(func=handle_step)

    show_parser = subparsers.add_parser('show')
    show_parser.add_argument('--state', required=True)
    show_parser.set_defaults(func=handle_show)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        # Default to interactive
        run_interactive(args)

def run_interactive(args):
    from roguelike.renderer import main as interactive_main
    interactive_main()

if __name__ == '__main__':
    main()
