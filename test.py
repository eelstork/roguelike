import subprocess
import os
import json
from roguelike.engine import Game

def run_cmd(args):
    return subprocess.run(['python3', '-m', 'roguelike'] + args, capture_output=True, text=True)

def test_engine():
    # Basic Move test
    game = Game(seed=42)
    start = game.player_pos
    game.step('right')
    assert game.player_pos == (start[0] + 1, start[1])

    # Win condition test
    game = Game(seed=42)
    items = list(game.items)
    for item in items:
        while game.player_pos[0] < item[0]: game.step('right')
        while game.player_pos[0] > item[0]: game.step('left')
        while game.player_pos[1] < item[1]: game.step('down')
        while game.player_pos[1] > item[1]: game.step('up')
        
    assert game.done is True
    assert game.outcome == "win"

    # Lose condition test (health)
    game = Game(seed=42)
    # Move until player hits monster 3 times
    for _ in range(100):
        if game.done: break
        game.step('down')
    
    assert game.player_health == 0
    assert game.done is True
    assert game.outcome == "lose"

def test_cli():
    tmp_file = "test_state.json"
    if os.path.exists(tmp_file):
        os.remove(tmp_file)

    try:
        # 1. Invoke step right
        res = run_cmd(['step', 'right', '--state', tmp_file])
        assert res.returncode == 0
        assert '@' in res.stdout
        assert os.path.exists(tmp_file)

        # 2. Invoke step repeatedly to collect items and verify count
        # Find item to collect
        with open(tmp_file, 'r') as f:
            data = json.load(f)
            # Item is at data['items'][0]
            target = data['items'][0]
        
        # Move to target
        curr_x, curr_y = data['player_pos']
        
        # Just loop steps until items are collected.
        items_at_start = 3
        prev_items = items_at_start
        
        while True:
            # We just need to move closer, let's just spam right/down
            res = run_cmd(['step', 'right', '--state', tmp_file])
            assert res.returncode == 0
            
            # Check items
            with open(tmp_file, 'r') as f:
                data = json.load(f)
            
            current_items_count = 3 - len(data['items'])
            if current_items_count > prev_items:
                # Verified increment
                break
            
            if data['done']:
                break
            prev_items = current_items_count
        
        assert current_items_count > 0

        # 3. Invalid action
        res = run_cmd(['step', 'jump', '--state', tmp_file])
        assert res.returncode != 0
        
    finally:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)

def test_round_trip():
    # Build a game, step several times into a state where player_health < 3
    # and at least one potion has been picked up
    
    # 1. Find a potion position
    g = Game(seed=123)
    potion_pos = g.potions[0]
    
    # Move player to potion
    while g.player_pos[0] < potion_pos[0]: g.step('right')
    while g.player_pos[0] > potion_pos[0]: g.step('left')
    while g.player_pos[1] < potion_pos[1]: g.step('down')
    while g.player_pos[1] > potion_pos[1]: g.step('up')
    
    # After picking up potion, player health should be 3 if it was full? 
    # Actually potion increases health. Let's make sure it's < 3 by moving into monster.
    
    # Move into monster at least once
    g.step('down')
    g.step('down')
    g.step('down')
    g.step('down')
    
    assert g.player_health < 3
    
    # Save
    data = g.to_dict()
    # Load
    g2 = Game.from_dict(data)
    
    # Render
    r1 = g.render()
    r2 = g2.render()
    
    assert r1 == r2
    
    # CLI version
    tmp_file = "roundtrip.json"
    try:
        with open(tmp_file, 'w') as f:
            json.dump(data, f)
            
        res = run_cmd(['show', '--state', tmp_file])
        assert res.returncode == 0
        assert res.stdout.strip() == r1.strip()
    finally:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)

if __name__ == "__main__":
    test_engine()
    test_cli()
    test_round_trip()
    print("All tests passed")
