import random

class Game:
    def __init__(self, width=20, height=20, seed=42):
        self.width = width
        self.height = height
        self.seed = seed
        self.rng = random.Random(seed)
        self._done = False
        self._outcome = ""
        self._turn = 0
        self.hp = 3
        self._player_pos = [1, 1]
        self._monster_pos = [width - 2, height - 2]
        
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
            
        self.items = []
        while len(self.items) < 3:
            ix = self.rng.randint(1, width - 2)
            iy = self.rng.randint(1, height - 2)
            if [ix, iy] != self._player_pos and [ix, iy] != self._monster_pos and [ix, iy] not in self.items:
                self.items.append([ix, iy])

    @property
    def player_pos(self):
        return tuple(self._player_pos)

    @property
    def monster_pos(self):
        return tuple(self._monster_pos)

    @property
    def done(self):
        return self._done

    @property
    def outcome(self):
        return self._outcome

    @property
    def turn(self):
        return self._turn

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

        self._turn += 1

        new_x = self._player_pos[0] + dx
        new_y = self._player_pos[1] + dy

        if 0 <= new_x < self.width and 0 <= new_y < self.height and self.map[new_y][new_x] != '#':
            self._player_pos = [new_x, new_y]

        # Pickup item
        if self._player_pos in self.items:
            self.items.remove(list(self._player_pos))
        
        # Monster move
        mx, my = self._monster_pos
        px, py = self._player_pos
        
        diff_x = px - mx
        diff_y = py - my
        
        move_x, move_y = 0, 0
        
        if abs(diff_x) >= abs(diff_y):
            if diff_x != 0:
                move_x = 1 if diff_x > 0 else -1
        else:
            if diff_y != 0:
                move_y = 1 if diff_y > 0 else -1
        
        # Check walls
        if self.map[my + move_y][mx + move_x] != '#':
            self._monster_pos = [mx + move_x, my + move_y]
        else:
            # If blocked, try the other axis
            if move_x != 0:
                if self.map[my + (1 if diff_y > 0 else -1)][mx] != '#':
                     self._monster_pos = [mx, my + (1 if diff_y > 0 else -1)]
            elif move_y != 0:
                if self.map[my][mx + (1 if diff_x > 0 else -1)] != '#':
                     self._monster_pos = [mx + (1 if diff_x > 0 else -1), my]

        # Conditions
        if self._monster_pos == self._player_pos:
            self.hp -= 1
            if self.hp <= 0:
                self._done = True
                self._outcome = "lose"
        elif not self.items:
            self._done = True
            self._outcome = "win"

    def render(self):
        status = f"turn: {self.turn}  items: {3-len(self.items)}/3  hp: {self.hp}  outcome: {self.outcome}"
        output = [status]
        for y in range(self.height):
            row = list(self.map[y])
            for item in self.items:
                if y == item[1]:
                    row[item[0]] = '*'
            if y == self._monster_pos[1]:
                row[self._monster_pos[0]] = 'M'
            if y == self._player_pos[1]:
                row[self._player_pos[0]] = '@'
            output.append("".join(row))
        return "\n".join(output)
