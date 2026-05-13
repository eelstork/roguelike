import argparse
import json
import os
import sys
from roguelike.engine import Game

def save_game(game, path):
    with open(path, 'w') as f:
        json.dump(game.to_dict(), f)

def load_game(path):
    if not os.path.exists(path):
        return Game()
    
    with open(path, 'r') as f:
        data = json.load(f)
    
    return Game.from_dict(data)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    step_parser = subparsers.add_parser('step')
    step_parser.add_argument('action', choices=['up', 'down', 'left', 'right', 'quit'])
    step_parser.add_argument('--state', required=True)

    show_parser = subparsers.add_parser('show')
    show_parser.add_argument('--state', required=True)

    play_parser = subparsers.add_parser('play')

    args = parser.parse_args()

    if args.command == 'step':
        game = load_game(args.state)
        game.step(args.action)
        save_game(game, args.state)
        print(game.render())
    elif args.command == 'show':
        game = load_game(args.state)
        print(game.render())
    else:
        # Default to play if no args or play command
        from roguelike import renderer
        renderer.main()

if __name__ == '__main__':
    main()
