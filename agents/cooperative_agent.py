from game.snake_agent import SnakeAgent

class CooperativeAgent(SnakeAgent):
    def __init__(self, id):
        super().__init__(id)
        self.allies = []

    def step(self, food_positions=None, other_snakes=None):
        if self.allies and food_positions:
            for ally in self.allies:
                ally.known_food = food_positions

        known_food = getattr(self, 'known_food', food_positions)
        if known_food:
            head_x, head_y = self.body[0]
            food_x, food_y = known_food[0]
            dx = 1 if food_x > head_x else -1 if food_x < head_x else 0
            dy = 1 if food_y > head_y else -1 if food_y < head_y else 0
            if dx != 0:
                self.direction = (dx, 0)
            elif dy != 0:
                self.direction = (0, dy)

        super().step(food_positions, other_snakes)
