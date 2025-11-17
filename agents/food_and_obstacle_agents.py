import random
from core.config import GRID_SIZE

class FoodAgent:
    def __init__(self, position, ftype="normal"):
        self.position = position
        self.type = ftype

class BonusAgent(FoodAgent):
    def __init__(self, position):
        super().__init__(position, ftype="bonus")

class PoisonAgent(FoodAgent):
    def __init__(self, position):
        super().__init__(position, ftype="poison")

class ObstacleAgent:
    def __init__(self, position):
        self.position = position

    def step(self):
        # random movement for obstacles
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        nx = max(0, min(GRID_SIZE - 1, self.position[0] + dx))
        ny = max(0, min(GRID_SIZE - 1, self.position[1] + dy))
        self.position = (nx, ny)
