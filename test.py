from roguelike.engine import Game

def test():
    game = Game(seed=42)
    start = game.player_pos
    
    actions = ['right', 'right', 'down', 'quit']
    for action in actions:
        game.step(action)
        
    assert game.done is True
    assert game.player_pos == (start[0] + 2, start[1] + 1)
    
    print("OK")

if __name__ == "__main__":
    test()
