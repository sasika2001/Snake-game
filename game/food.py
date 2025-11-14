import pygame
import random
from core.config import GRID_SIZE, CELL_SIZE

class Food:
    TYPES = [
        {"color": (255, 255, 0), "score": 1},  # Normal food
        {"color": (0, 255, 255), "score": 2},  # Bonus food
        {"color": (255, 0, 255), "score": -1}  # Poison (reduces score)
    ]

    def __init__(self):
        self.random_food()

    def random_food(self):
        self.type = random.choice(Food.TYPES)
        self.color = self.type["color"]
        self.score_value = self.type["score"]
        self.position = self.random_position()

    def random_position(self):
        return (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))

    def update(self, snake_heads=None):
        if snake_heads and self.position in snake_heads:
            self.random_food()

    def draw(self, screen):
        x, y = self.position
        pygame.draw.rect(screen, self.color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
