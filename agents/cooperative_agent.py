import random
from collections import deque
from core import config

GRID_SIZE = config.GRID_SIZE


class CooperativeAIAgent:
    def __init__(self, id, start_pos=(10,10), color=(50,150,255)):
        self.id = id
        self.body = [start_pos]
        self.direction = "LEFT"
        self.alive = True
        self.score = 0
        self.color = color
        self.memory = deque(maxlen=20)
        self.intent = None
        self.cooperative = True  # This agent always cooperates
        self.sensing_range = config.BASE_SENSING_RANGE

        # Personality for decision-making
        self.personality = {
            "fear": 0.5,
            "hunger": 0.8,
            "curiosity": 0.3,
            "cooperation": 1.2   # Boost cooperative behavior
        }

        # Store last perception
        self.last_perception = {"food":[], "snakes":[], "obstacles":[], "shared_danger":[]}

    # -----------------------------
    # Perception
    # -----------------------------
    def perceive(self, food_positions, other_snakes, obstacles, env):
        hx, hy = self.body[0]

        visible_food = [p for p in food_positions
                        if abs(p[0] - hx) <= self.sensing_range and abs(p[1] - hy) <= self.sensing_range]

        visible_snakes = []
        for s in other_snakes:
            for seg in s.body:
                if abs(seg[0] - hx) <= self.sensing_range and abs(seg[1] - hy) <= self.sensing_range:
                    visible_snakes.append(seg)

        visible_obstacles = [o for o in obstacles
                             if abs(o[0] - hx) <= self.sensing_range and abs(o[1] - hy) <= self.sensing_range]

        shared = getattr(env, "shared_dangers", set())
        shared_visible = [d for d in shared
                          if abs(d[0] - hx) <= self.sensing_range and abs(d[1] - hy) <= self.sensing_range]

        self.last_perception = {
            "food": visible_food,
            "snakes": visible_snakes,
            "obstacles": visible_obstacles,
            "shared_danger": shared_visible
        }

    # -----------------------------
    # Helpers
    # -----------------------------
    def neighbors(self, pos):
        x,y = pos
        dirs = [(0,-1,"UP"),(0,1,"DOWN"),(-1,0,"LEFT"),(1,0,"RIGHT")]
        for dx,dy,dirc in dirs:
            nx, ny = x+dx, y+dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                yield (nx,ny), dirc

    def risk_score(self, pos, obstacles, other_snakes, env):
        # Danger from obstacles
        obstacle_dist = min([abs(pos[0]-o[0])+abs(pos[1]-o[1]) for o in obstacles] + [999])

        # Danger from snake bodies
        snake_dists = [abs(pos[0]-seg[0])+abs(pos[1]-seg[1]) for s in other_snakes for seg in s.body]
        nearest_snake = min(snake_dists) if snake_dists else 999

        # Shared danger broadcast
        shared = getattr(env, "shared_dangers", set())
        shared_pen = 5.0 if tuple(pos) in shared else 0.0

        risk = 0
        risk += 0 if obstacle_dist > 5 else (6 - obstacle_dist) * 0.5
        risk += 0 if nearest_snake > 5 else (6 - nearest_snake) * 0.8
        risk += shared_pen

        return risk

    def safe_moves(self, other_snakes, obstacles):
        safe = []
        head = self.body[0]
        for neigh, dirc in self.neighbors(head):
            if neigh in obstacles:
                continue
            if neigh in self.body:
                continue
            if any(neigh in s.body for s in other_snakes):
                continue
            safe.append((neigh, dirc))
        return safe

    # -----------------------------
    # Cooperative decision making
    # -----------------------------
    def decide(self, food_positions, food_types, other_snakes, obstacles, env):
        head = self.body[0]

        # Cooperative food sharing — avoid food another teammate sees
        coop_targets = set()
        for agent in env.ai_list:
            if agent is not self and agent.cooperative:
                coop_targets.update(agent.last_perception.get("food", []))

        best_move = None
        best_score = -999

        for neigh, dirc in self.neighbors(head):
            risk = self.risk_score(neigh, obstacles, other_snakes, env)

            food_bonus = 0
            if neigh in food_positions:
                ftype = food_types.get(neigh, "normal")
                if ftype == "bonus":
                    food_bonus = 4
                elif ftype == "poison":
                    food_bonus = -3
                else:
                    food_bonus = 1

                # Cooperation penalty
                if neigh in coop_targets:
                    food_bonus -= 1.5

            # Utility
            score = (
                food_bonus * self.personality["hunger"]
                - risk * self.personality["fear"]
                + random.uniform(-0.02, 0.02)
            )

            if score > best_score:
                best_score = score
                best_move = dirc

        if best_move:
            return best_move

        # If no good moves → choose safest among safe moves
        safe = self.safe_moves(other_snakes, obstacles)
        if safe:
            return safe[0][1]

        return self.direction

    # -----------------------------
    # Broadcast danger if surrounded
    # -----------------------------
    def maybe_broadcast_danger(self, env):
        if len(self.last_perception.get("snakes", [])) > 5:
            env.broadcast({"type": "danger", "from": self.id, "pos": self.body[0]})
            env.log_event("broadcast", "danger", self.id, self.body[0])

    # -----------------------------
    # Step execution
    # -----------------------------
    def step(self, food_positions, food_types, other_snakes, obstacles, env):
        if not self.alive:
            return []

        # Perception
        self.perceive(food_positions, other_snakes, obstacles, env)

        # Decide next direction
        chosen = self.decide(food_positions, food_types, other_snakes, obstacles, env)
        self.direction = chosen
        self.maybe_broadcast_danger(env)

        # Movement
        dir_to_delta = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0),
        }

        dx, dy = dir_to_delta.get(chosen, (0,0))
        new_head = (self.body[0][0] + dx, self.body[0][1] + dy)

        # Boundary correction
        new_head = (
            max(0, min(GRID_SIZE-1, new_head[0])),
            max(0, min(GRID_SIZE-1, new_head[1]))
        )

        # Collision detection
        if (
            new_head in obstacles
            or new_head in self.body
            or any(new_head in s.body for s in other_snakes)
        ):
            self.alive = False
            env.log_event("collision", "coop_agent_died", self.id, new_head)
            return []

        self.body.insert(0, new_head)

        # Food eating
        events = []
        if new_head in food_positions:
            ftype = food_types.get(new_head, "normal")
            if ftype == "bonus":
                self.score += 3
            elif ftype == "poison":
                self.score = max(0, self.score - 2)
            else:
                self.score += 1

            events.append(("ate", self.id, new_head, ftype))
            env.log_event("eat", "coop_agent_ate", self.id, new_head)

        else:
            self.body.pop()

        self.memory.append(new_head)
        return events
