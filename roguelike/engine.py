import random

class Game:
    def __init__(self, width=20, height=20, seed=42):
        self.width = width
        self.height = height
        self.seed = seed
        self._done = False
        self._player_pos = [width // 2, height // 2]
        
        # Initialize map
        self.map = []
        for y in range(height):
            row = []
            for x in range(width):
                if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                    row.append('#')
                else:
                    row.append('.')
            self.map.append(row)

    @property
    def player_pos(self):
        return tuple(self._player_pos)

    @property
    def done(self):
        return self._done

    def step(self, action):
        if self._done:
            return

        if action == 'quit':
            self._done = True
            return

        dx, dy = 0, 0
        if action == 'up':
            dy = -1
        elif action == 'down':
            dy = 1
        elif action == 'left':
            dx = -1
        elif action == 'right':
            dx = 1
        else:
            return

        new_x = self._player_pos[0] + dx
        new_y = self._player_pos[1] + dy

        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            if self.map[new_y][new_x] != '#':
                self._player_pos = [new_x, new_y]

    def render(self):
        output = []
        for y in range(self.height):
            row = list(self.map[y])
            if y == self._player_pos[1]:
                row[self._player_pos[0]] = '@'
            output.append("".join(row))
        return "\n".join(output)
