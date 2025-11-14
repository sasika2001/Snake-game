from game.snake_agent import SnakeAgent

class CompetitiveAgent(SnakeAgent):
    def __init__(self, id):
        super().__init__(id)

    def step(self, food_positions=None, other_snakes=None):
        target_head = None
        for snake in other_snakes or []:
            if snake.alive:
                distance = abs(self.body[0][0]-snake.body[0][0]) + abs(self.body[0][1]-snake.body[0][1])
                if distance <= 5:
                    target_head = snake.body[0]
                    break

        if target_head:
            head_x, head_y = self.body[0]
            tx, ty = target_head
            dx = 1 if tx > head_x else -1 if tx < head_x else 0
            dy = 1 if ty > head_y else -1 if ty < head_y else 0
            if dx != 0:
                self.direction = (dx, 0)
            elif dy != 0:
                self.direction = (0, dy)
        elif food_positions:
            head_x, head_y = self.body[0]
            fx, fy = food_positions[0]
            dx = 1 if fx > head_x else -1 if fx < head_x else 0
            dy = 1 if fy > head_y else -1 if fy < head_y else 0
            if dx != 0:
                self.direction = (dx, 0)
            elif dy != 0:
                self.direction = (0, dy)

        super().step(food_positions, other_snakes)
