import heapq
import random
from collections import deque
from core import config

GRID_SIZE = config.GRID_SIZE


class CognitiveAIAgent:
    def __init__(self, id, start_pos=(10, 10), color=(200, 0, 0), cooperative=False, personality=None):
        self.id = id
        self.body = [start_pos]
        self.alive = True
        self.score = 0
        self.direction = "LEFT"
        self.memory = deque(maxlen=24)  # short-term memory of recent positions
        self.sensing_range = config.BASE_SENSING_RANGE
        self.smartness = config.BASE_SMARTNESS
        self.color = color
        self.cooperative = cooperative

        # Personality/emotion defaults
        self.personality = personality or {"fear": 0.6, "hunger": 1.0, "aggression": 0.4, "curiosity": 0.3}

        self.intent = None
        self.planned_path = []
        self.last_perception = {"food": [], "snakes": [], "obstacles": [], "shared_danger": []}

    # -------------------------
    # Perception
    # -------------------------
    def perceive(self, food_positions, other_snakes, obstacles, env):
        hx, hy = self.body[0]
        visible_food = [
            p for p in food_positions if abs(p[0] - hx) <= self.sensing_range and abs(p[1] - hy) <= self.sensing_range
        ]
        visible_snakes = []
        for s in other_snakes:
            if not getattr(s, "alive", True):
                continue
            visible_snakes += [
                seg for seg in getattr(s, "body", []) if abs(seg[0] - hx) <= self.sensing_range and abs(seg[1] - hy) <= self.sensing_range
            ]
        visible_obstacles = [o for o in obstacles if abs(o[0] - hx) <= self.sensing_range and abs(o[1] - hy) <= self.sensing_range]

        shared = getattr(env, "shared_dangers", set())
        shared_visible = [d for d in shared if abs(d[0] - hx) <= self.sensing_range and abs(d[1] - hy) <= self.sensing_range]

        self.last_perception = {"food": visible_food, "snakes": visible_snakes, "obstacles": visible_obstacles, "shared_danger": shared_visible}

    # -------------------------
    # Grid helpers
    # -------------------------
    def neighbors(self, pos):
        x, y = pos
        for dx, dy, dirc in [(0, -1, "UP"), (0, 1, "DOWN"), (-1, 0, "LEFT"), (1, 0, "RIGHT")]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                yield (nx, ny), dirc

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # -------------------------
    # A* pathfinding
    # -------------------------
    def astar(self, start, goal, blocked_set):
        open_heap = []
        heapq.heappush(open_heap, (self.heuristic(start, goal), 0, start))
        came_from = {}
        gscore = {start: 0}
        closed = set()

        while open_heap:
            f, g, current = heapq.heappop(open_heap)
            if current in closed:
                continue
            closed.add(current)
            if current == goal:
                path = []
                node = current
                while node != start:
                    path.append(node)
                    node = came_from[node]
                path.reverse()
                return path
            for neigh, _dir in self.neighbors(current):
                if neigh in blocked_set:
                    continue
                tentative_g = g + 1
                if tentative_g < gscore.get(neigh, 1e9):
                    came_from[neigh] = current
                    gscore[neigh] = tentative_g
                    heapq.heappush(open_heap, (tentative_g + self.heuristic(neigh, goal), tentative_g, neigh))
        return []

    # -------------------------
    # Flood-fill reachable count
    # -------------------------
    def flood_fill_size(self, start, blocked_set, limit=400):
        q = [start]
        seen = {start}
        idx = 0
        while idx < len(q) and len(seen) < limit:
            pos = q[idx]
            idx += 1
            for neigh, _d in self.neighbors(pos):
                if neigh in seen or neigh in blocked_set:
                    continue
                seen.add(neigh)
                q.append(neigh)
        return len(seen)

    # -------------------------
    # Risk scoring
    # -------------------------
    def risk_score(self, cell, other_snakes, obstacles, env):
        ox_dist = min([abs(cell[0] - o[0]) + abs(cell[1] - o[1]) for o in obstacles] + [999])
        snake_seg_dists = [abs(cell[0] - seg[0]) + abs(cell[1] - seg[1]) for s in other_snakes for seg in getattr(s, "body", [])]
        nearest_snake = min(snake_seg_dists) if snake_seg_dists else 999
        shared = getattr(env, "shared_dangers", set())
        shared_pen = 0 if tuple(cell) not in shared else 5.0
        enemy_heads = [s.body[0] for s in other_snakes if getattr(s, "body", [])]
        head_dists = [abs(cell[0] - h[0]) + abs(cell[1] - h[1]) for h in enemy_heads] if enemy_heads else [999]
        nearest_head = min(head_dists)
        r = 0.0
        r += 0 if ox_dist > 6 else (6 - ox_dist) * 0.5
        r += 0 if nearest_snake > 6 else (6 - nearest_snake) * 0.8
        r += 0 if nearest_head > 4 else (5 - nearest_head) * 1.5
        r += shared_pen
        return r

    # -------------------------
    # Safe neighbor moves
    # -------------------------
    def safe_moves(self, other_snakes, obstacles):
        head = self.body[0]
        safe = []
        for neigh, dirc in self.neighbors(head):
            collision = neigh in obstacles or neigh in self.body or any(neigh in getattr(s, "body", []) for s in other_snakes)
            if not collision:
                safe.append((neigh, dirc))
        return safe

    # -------------------------
    # Decision-making
    # -------------------------
    def decide(self, food_positions, food_types, other_snakes, obstacles, env):
        head = self.body[0]

        # Follow planned path if valid
        if self.planned_path:
            next_pos = self.planned_path[0]
            blocked = set(obstacles) | set(self.memory) | set(seg for s in other_snakes for seg in getattr(s, "body", []))
            if next_pos not in blocked:
                next_step = self.planned_path.pop(0)
                dx = next_step[0] - head[0]; dy = next_step[1] - head[1]
                if dx == 1: return "RIGHT"
                if dx == -1: return "LEFT"
                if dy == 1: return "DOWN"
                if dy == -1: return "UP"
            else:
                self.planned_path = []

        blocked_set = set(obstacles) | set(self.memory) | set(seg for s in other_snakes for seg in getattr(s, "body", []))

        if not food_positions:
            safe = self.safe_moves(other_snakes, obstacles)
            if not safe:
                return self.direction
            best_dir = safe[0][1]
            best_sz = -1
            for np, dirc in safe:
                sz = self.flood_fill_size(np, blocked_set)
                if sz > best_sz:
                    best_sz = sz
                    best_dir = dirc
            return best_dir

        # Cooperative awareness
        coop_targets = set()
        if self.cooperative:
            for a in getattr(env, "ai_list", []):
                if a is not self and getattr(a, "cooperative", False):
                    for f in getattr(a, "last_perception", {}).get("food", []):
                        coop_targets.add(f)

        # Evaluate foods
        best_move = None
        best_score = -1e9
        for food in food_positions:
            path = self.astar(head, food, blocked_set)
            if not path:
                continue
            next_cell = path[0]
            risk = self.risk_score(next_cell, other_snakes, obstacles, env)
            space = self.flood_fill_size(next_cell, blocked_set)
            dist = len(path)
            ftype = food_types.get(food, "normal")
            fval = 3.0 if ftype=="bonus" else (-2.0 if ftype=="poison" else 1.0)
            fear = self.personality.get("fear",0.6)
            hunger = self.personality.get("hunger",1.0)
            aggression = self.personality.get("aggression",0.4)
            curiosity = self.personality.get("curiosity",0.3)
            coop_pen = -1.5 if food in coop_targets else 0.0
            utility = (hunger*(fval/(1+dist))) + (curiosity*(space/(GRID_SIZE*GRID_SIZE))) - (fear*risk) + (aggression*(1/(1+dist))) + coop_pen
            utility += random.uniform(-0.01,0.01)
            if utility > best_score:
                best_score = utility
                best_move = (path, next_cell)

        if best_move:
            path, next_cell = best_move
            self.planned_path = path[1:] if len(path)>1 else []
            dx = next_cell[0] - head[0]; dy = next_cell[1] - head[1]
            if dx == 1: return "RIGHT"
            if dx == -1: return "LEFT"
            if dy == 1: return "DOWN"
            if dy == -1: return "UP"

        safe = self.safe_moves(other_snakes, obstacles)
        if safe:
            best_dir = safe[0][1]; best_val = -1e9
            for np, dirc in safe:
                sz = self.flood_fill_size(np, blocked_set)
                r = self.risk_score(np, other_snakes, obstacles, env)
                val = (self.personality.get("curiosity",0.3)*sz) - (self.personality.get("fear",0.6)*r) + random.uniform(-0.01,0.01)
                if val > best_val:
                    best_val = val
                    best_dir = dirc
            return best_dir

        return self.direction

    # -------------------------
    # Step: perceive -> decide -> act
    # -------------------------
    def step(self, food_positions, food_types, other_snakes, obstacles, env):
        if not self.alive:
            return []

        self.perceive(food_positions, other_snakes, obstacles, env)
        chosen_dir = self.decide(food_positions, food_types, other_snakes, obstacles, env)
        self.intent = chosen_dir

        dir_to_delta = {"UP": (0,-1),"DOWN":(0,1),"LEFT":(-1,0),"RIGHT":(1,0)}
        dx, dy = dir_to_delta.get(chosen_dir,(0,0))
        new_head = (self.body[0][0]+dx, self.body[0][1]+dy)
        new_head = (max(0,min(GRID_SIZE-1,new_head[0])), max(0,min(GRID_SIZE-1,new_head[1])))

        # collision
        if new_head in self.body or new_head in obstacles or any(new_head in getattr(s,"body",[]) for s in other_snakes):
            self.alive = False
            return []

        self.body.insert(0,new_head)
        ate=False
        eaten_type=None
        if new_head in food_positions:
            ate=True
            eaten_type=food_types.get(new_head,"normal")
            if eaten_type=="bonus":
                self.score+=3
            elif eaten_type=="poison":
                self.score=max(0,self.score-2)
            else:
                self.score+=1
        else:
            self.body.pop()

        self.memory.append(new_head)
        events=[]
        if ate:
            events.append(("ate",self.id,new_head,eaten_type))
        return events
