from roguelike.engine import Game

def test():
    # Test default
    game = Game(seed=42)
    assert game.width == 20
    assert game.height == 20
    
    # Test custom size
    game = Game(30, 40, seed=42)
    assert game.width == 30
    assert game.height == 40
    
    # Test gameplay with custom size
    start = game.player_pos
    
    actions = ['right', 'right', 'down', 'quit']
    for action in actions:
        game.step(action)
        
    assert game.done is True
    # Initial position for (30, 40) is (15, 20)
    assert game.player_pos == (start[0] + 2, start[1] + 1)
    
    print("OK")

if __name__ == "__main__":
    test()
