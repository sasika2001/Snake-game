import pygame
from core.config import GRID_SIZE

class HumanAgent:
    def __init__(self, id, start_pos=(5,5), color=(0,200,0)):
        self.id = id
        self.body = [start_pos]           # Snake segments
        self.alive = True
        self.score = 0
        self.direction = 'RIGHT'
        self.color = color

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_UP and self.direction != 'DOWN':
            self.direction = 'UP'
        elif event.key == pygame.K_DOWN and self.direction != 'UP':
            self.direction = 'DOWN'
        elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def next_position(self):
        x, y = self.body[0]
        if self.direction == 'UP': y -= 1
        elif self.direction == 'DOWN': y += 1
        elif self.direction == 'LEFT': x -= 1
        elif self.direction == 'RIGHT': x += 1
        # Clamp within grid
        x = max(0, min(GRID_SIZE - 1, x))
        y = max(0, min(GRID_SIZE - 1, y))
        return (x, y)

    def step(self, food_positions, food_types, obstacles):
        if not self.alive:
            return

        new_head = self.next_position()

        # Check collisions with self or obstacles
        if new_head in self.body or new_head in obstacles:
            self.alive = False
            return

        # Add new head
        self.body.insert(0, new_head)

        # Handle food
        if new_head in food_positions:
            ftype = food_types.get(new_head, 'normal')
            if ftype == 'normal':
                self.score += 1
            elif ftype == 'bonus':
                self.score += 3
            elif ftype == 'poison':
                self.score = max(0, self.score - 2)
            
            # Remove eaten food
            idx = food_positions.index(new_head)
            food_positions.pop(idx)
            food_types.pop(new_head, None)

        # Adjust snake length based on score
        target_length = max(1, self.score + 1)  # minimum length = 1
        while len(self.body) > target_length:
            self.body.pop()
