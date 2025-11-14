import random
from collections import deque
from queue import Queue
from core import config

GRID_SIZE = config.GRID_SIZE
BASE_SENSING = config.BASE_SENSING_RANGE

class CognitiveAIAgent:
    def __init__(self, id, start_pos=(10,10), color=(200,0,0)):
        self.id = id
        self.body = [start_pos]
        self.alive = True
        self.score = 0
        self.direction = 'LEFT'
        self.memory = deque(maxlen=12)
        self.sensing_range = BASE_SENSING
        self.smartness = config.BASE_SMARTNESS
        self.color = color

    def perceive(self, food_positions, other_snakes, obstacles):
        hx, hy = self.body[0]
        visible_food = [p for p in food_positions if abs(p[0]-hx)<=self.sensing_range and abs(p[1]-hy)<=self.sensing_range]
        visible_snakes = []
        for s in other_snakes:
            if not s.alive: continue
            visible_snakes += [seg for seg in s.body if abs(seg[0]-hx)<=self.sensing_range and abs(seg[1]-hy)<=self.sensing_range]
        visible_obstacles = [o for o in obstacles if abs(o[0]-hx)<=self.sensing_range and abs(o[1]-hy)<=self.sensing_range]
        self.perception = {'food': visible_food, 'snakes': visible_snakes, 'obstacles': visible_obstacles}

    def next_pos_from_dir(self, direction):
        x, y = self.body[0]
        if direction == 'UP': y -= 1
        if direction == 'DOWN': y += 1
        if direction == 'LEFT': x -= 1
        if direction == 'RIGHT': x += 1
        x = max(0, min(GRID_SIZE-1, x))
        y = max(0, min(GRID_SIZE-1, y))
        return (x, y)

    def bfs_path(self, target, other_snakes, obstacles):
        start = self.body[0]
        obstacles_set = set(obstacles + list(self.memory) + [seg for s in other_snakes for seg in s.body])
        q = Queue()
        q.put((start, []))
        visited = set()
        while not q.empty():
            pos, path = q.get()
            if pos in visited: continue
            visited.add(pos)
            if pos == target: return path
            for move, delta in [('UP',(0,-1)),('DOWN',(0,1)),('LEFT',(-1,0)),('RIGHT',(1,0))]:
                nx, ny = pos[0]+delta[0], pos[1]+delta[1]
                if 0<=nx<GRID_SIZE and 0<=ny<GRID_SIZE:
                    np = (nx, ny)
                    if np in obstacles_set: continue
                    if np in visited: continue
                    q.put((np, path+[move]))
        return []

    def plan_move(self, human, food_positions, other_snakes, obstacles):
        if self.smartness <= 1:
            for f in self.perception['food']:
                if abs(f[0]-self.body[0][0]) + abs(f[1]-self.body[0][1]) == 1:
                    dx=f[0]-self.body[0][0]; dy=f[1]-self.body[0][1]
                    if dx==1: return 'RIGHT'
                    if dx==-1: return 'LEFT'
                    if dy==1: return 'DOWN'
                    if dy==-1: return 'UP'
            moves=['UP','DOWN','LEFT','RIGHT']
            random.shuffle(moves)
            for m in moves:
                np=self.next_pos_from_dir(m)
                if np in obstacles or any(np in s.body for s in other_snakes) or np in self.body: continue
                return m
            return random.choice(['UP','DOWN','LEFT','RIGHT'])
        if self.perception['food']:
            target=min(self.perception['food'], key=lambda p: abs(p[0]-self.body[0][0])+abs(p[1]-self.body[0][1]))
            path=self.bfs_path(target, other_snakes, obstacles)
            if path: return path[0]
        moves=['UP','DOWN','LEFT','RIGHT']
        random.shuffle(moves)
        for m in moves:
            np=self.next_pos_from_dir(m)
            if np in obstacles or any(np in s.body for s in other_snakes) or np in self.body: continue
            return m
        return random.choice(['UP','DOWN','LEFT','RIGHT'])

    def step(self, food_positions, food_types, other_snakes, obstacles):
        if not self.alive: return
        self.perceive(food_positions, other_snakes, obstacles)
        human = other_snakes[0]
        move=self.plan_move(human, food_positions, other_snakes, obstacles)
        self.direction = move
        new_head=self.next_pos_from_dir(move)
        if new_head in self.body or new_head in obstacles or any(new_head in s.body for s in other_snakes if s.id!=self.id):
            self.alive=False
            return
        self.body.insert(0,new_head)
        if new_head in food_positions:
            ft=food_types.get(new_head,'normal')
            if ft=='normal': self.score+=1
            elif ft=='bonus': self.score+=3
            elif ft=='poison': self.score=max(0,self.score-2)
            idx=food_positions.index(new_head)
            food_positions.pop(idx)
            food_types.pop(new_head,None)
        else: self.body.pop()
        self.memory.append(new_head)
