import pygame
import random
from core.config import CELL_SIZE, GRID_SIZE

class SnakeAgent:
    COLORS = [(0, 255, 0), (255, 0, 0)]  # Human green, AI red

    def __init__(self, id, start_pos):
        self.id = id
        self.body = [start_pos]
        self.color = SnakeAgent.COLORS[id % len(SnakeAgent.COLORS)]
        self.direction = (1, 0)
        self.grow_pending = 0
        self.alive = True
        self.score = 0
        self.env = None  # reference to environment

    def step(self, food_positions=None, other_snakes=None):
        if not self.alive:
            return

        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Collisions with walls
        if not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
            self.alive = False
            return

        # Collisions with itself
        if new_head in self.body:
            self.alive = False
            return

        # Collisions with other snakes
        if other_snakes:
            for snake in other_snakes:
                if snake.id != self.id and new_head in snake.body:
                    self.alive = False
                    return

        # Collisions with obstacles
        if self.env and new_head in getattr(self.env, 'obstacles', []):
            self.alive = False
            return

        # Move
        self.body.insert(0, new_head)

        # Check food
        if self.env and new_head == self.env.food.position:
            self.grow_pending += 1
            self.score += self.env.food.score_value
            self.env.food.random_food()

        # Remove tail if not growing
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def draw(self, screen):
        for segment in self.body:
            x, y = segment
            pygame.draw.rect(screen, self.color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def get_next_head(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        return (head_x + dx, head_y + dy)
