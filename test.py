import subprocess
import os
import sys

# Add current directory to path so we can import roguelike
sys.path.append(os.getcwd())

from roguelike.engine import Game

def test_engine():
    game = Game(seed=42)
    start = game.player_pos
    
    actions = ['right', 'right', 'down', 'quit']
    for action in actions:
        game.step(action)
        
    assert game.done is True
    assert game.player_pos == (start[0] + 2, start[1] + 1)
    print("Engine tests passed.")

def test_cli():
    state_path = "test_state.json"
    if os.path.exists(state_path):
        os.remove(state_path)
    
    try:
        # Step 1: Initialize/Step
        result = subprocess.run(
            [sys.executable, '-m', 'roguelike', 'step', 'right', '--state', state_path],
            capture_output=True, text=True, check=True
        )
        assert "@" in result.stdout
        
        # Step 2: Show
        result = subprocess.run(
            [sys.executable, '-m', 'roguelike', 'show', '--state', state_path],
            capture_output=True, text=True, check=True
        )
        assert "@" in result.stdout
        
        # Step 3: Invalid action
        result = subprocess.run(
            [sys.executable, '-m', 'roguelike', 'step', 'jump', '--state', state_path],
            capture_output=True, text=True, check=False
        )
        assert result.returncode != 0
        
        print("CLI tests passed.")
    finally:
        if os.path.exists(state_path):
            os.remove(state_path)

if __name__ == "__main__":
    test_engine()
    test_cli()
