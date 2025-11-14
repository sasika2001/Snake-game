from game.snake_agent import SnakeAgent
from core.config import GRID_SIZE

class AIAgent(SnakeAgent):
    def __init__(self, id, start_pos):
        super().__init__(id, start_pos)

    def step(self, food_positions=None, other_snakes=None):
        if not self.alive:
            return

        head_x, head_y = self.body[0]
        possible_dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        safe_moves = []

        # Determine safe moves
        for dx, dy in possible_dirs:
            new_head = (head_x + dx, head_y + dy)
            if not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
                continue
            collision = False
            for snake in other_snakes + [self]:
                if new_head in snake.body:
                    collision = True
                    break
            if self.env and new_head in getattr(self.env, 'obstacles', []):
                collision = True
            if not collision:
                safe_moves.append((dx, dy))

        # Move toward food safely
        if safe_moves and food_positions:
            food_x, food_y = food_positions[0]
            best_move = min(safe_moves, key=lambda d: abs((head_x+d[0])-food_x)+abs((head_y+d[1])-food_y))
            self.direction = best_move
        elif safe_moves:
            self.direction = safe_moves[0]

        super().step(food_positions, other_snakes)
