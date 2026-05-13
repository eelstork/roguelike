from roguelike.engine import Game

def test():
    # Basic Move test
    game = Game(seed=42)
    start = game.player_pos
    game.step('right')
    assert game.player_pos == (start[0] + 1, start[1])

    # Win condition test
    # Items were at (14, 15), (7, 13), (11, 4) with seed 42
    # Player at (10, 10)
    game = Game(seed=42)
    # Collect items
    # Items positions (found by printing them if needed, but let's just make sure we collect them)
    # Let's just play to win by walking over them
    # Actually it's better to verify the items list.
    
    game = Game(seed=42)
    # Items are at:
    items = list(game.items)
    for item in items:
        # Simple pathfinding to item
        while game.player_pos[0] < item[0]: game.step('right')
        while game.player_pos[0] > item[0]: game.step('left')
        while game.player_pos[1] < item[1]: game.step('down')
        while game.player_pos[1] > item[1]: game.step('up')
        
    assert game.done is True
    assert game.outcome == "win"

    # Lose condition test
    game = Game(seed=42)
    # Monster moves to player, player stands still
    while not game.done:
        game.step('up') # player moves up
        
    assert game.done is True
    assert game.outcome == "lose"
    
    print("All tests passed")

if __name__ == "__main__":
    test()
