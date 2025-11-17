# game/environment.py
import pygame, random, math, csv, os
from core.config import GRID_SIZE, CELL_SIZE, FOOD_PULSE_SPEED, FOOD_PULSE_AMPLITUDE, FONT_NAME, EVENT_LOG_PATH
from agents.food_and_obstacle_agents import FoodAgent, BonusAgent, PoisonAgent, ObstacleAgent

def load_sound(path):
    try:
        s = pygame.mixer.Sound(path)
        s.set_volume(0.5)
        return s
    except Exception:
        return None

class Environment:
    def __init__(self, human, ai_list, seed=None):
        self.human = human
        self.ai_list = ai_list
        self.food_agents = []
        self.obstacle_agents = []
        self.pulse_offset = 0.0
        self.font = pygame.font.SysFont(FONT_NAME, 18)
        self.eat_sound = load_sound('assets/sounds/eat.wav')
        self.levelup_sound = load_sound('assets/sounds/levelup.wav')
        self.gameover_sound = load_sound('assets/sounds/gameover.wav')
        self.shared_dangers = set()
        self.event_log = []
        self.step_count = 0
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        self.spawn_food_initial()
        if not os.path.exists('events'):
            os.makedirs('events')

        self.obstacle_move_counter = 0  # slow obstacle movement

    # -------------------------
    # Event log & broadcast
    # -------------------------
    def log_event(self, kind, action, agent_id, pos=None, extra=None):
        self.event_log.append({'step': self.step_count, 'kind': kind, 'action': action, 'agent': agent_id, 'pos': pos, 'extra': extra})

    def broadcast(self, msg):
        if msg['type'] == 'danger':
            self.shared_dangers.add(tuple(msg['pos']))
            self.log_event('broadcast', 'danger_broadcast', msg.get('from'), tuple(msg.get('pos')))

    # -------------------------
    # Spawning
    # -------------------------
    def spawn_food_initial(self):
        """Spawn 3 foods at the start (mix of normal, bonus, poison)"""
        self.food_agents = []
        while len(self.food_agents) < 3:
            self.spawn_food(1)

    def spawn_food(self, count=1):
        for _ in range(count):
            tries = 0
            while True:
                p = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
                if p not in self.all_occupied():
                    r = random.random()
                    if r < 0.7:
                        f = FoodAgent(p)
                        f.type = 'normal'
                    elif r < 0.9:
                        f = BonusAgent(p)
                        f.type = 'bonus'
                        f.lifetime = 300  # bonus disappears after 300 steps
                    else:
                        f = PoisonAgent(p)
                        f.type = 'poison'
                    self.food_agents.append(f)
                    self.log_event('spawn','food_spawned', None, p, extra={'type': f.type})
                    break
                tries += 1
                if tries > 200: break

    def spawn_obstacles(self, count=3):
        added = 0
        attempts = 0
        while added < count and attempts < 300:
            p = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
            if p not in self.all_occupied():
                self.obstacle_agents.append(ObstacleAgent(p))
                added += 1
                self.log_event('spawn','obstacle_spawned', None, p)
            attempts += 1

    # -------------------------
    # Helpers
    # -------------------------
    def all_occupied(self):
        occ = []
        occ += list(self.human.body)
        for a in self.ai_list:
            occ += list(a.body)
        for o in self.obstacle_agents:
            occ.append(o.position)
        for f in self.food_agents:
            occ.append(f.position)
        return occ

    # -------------------------
    # Step function
    # -------------------------
    def step(self, level):
        self.step_count += 1
        self.pulse_offset += 1.0 / FOOD_PULSE_SPEED

        # human acts
        self.human.step([f.position for f in self.food_agents], {f.position: f.type for f in self.food_agents}, [o.position for o in self.obstacle_agents])

        # AI acts
        for ai in self.ai_list:
            events = ai.step([f.position for f in self.food_agents],
                             {f.position: f.type for f in self.food_agents},
                             [self.human] + [x for x in self.ai_list if x is not ai],
                             [o.position for o in self.obstacle_agents], self)
            for e in events:
                pass

        # centralized eating
        eaten_positions = []
        for agent in [self.human] + self.ai_list:
            head = agent.body[0] if agent.alive else None
            if head:
                for f in self.food_agents:
                    if head == f.position:
                        eaten_positions.append((agent, f))
                        break
        for agent, food in eaten_positions:
            if food in self.food_agents:
                self.food_agents.remove(food)
            if self.eat_sound:
                try: self.eat_sound.play()
                except: pass
            agent.score += 3 if food.type=='bonus' else -2 if food.type=='poison' else 1
            self.log_event('eat','food_eaten', agent.id, food.position, extra={'type': food.type})

        # update bonus food lifetime
        for f in self.food_agents[:]:
            if f.type == 'bonus':
                if hasattr(f, 'lifetime'):
                    f.lifetime -= 1
                    if f.lifetime <= 0:
                        self.food_agents.remove(f)
        # ensure max 3 foods
        while len(self.food_agents) < 3:
            self.spawn_food(1)

        # obstacles move slowly
        self.obstacle_move_counter += 1
        if self.obstacle_move_counter >= 10:  # move every 10 steps
            self.obstacle_move_counter = 0
            for obs in self.obstacle_agents:
                old = obs.position
                obs.step()
                self.log_event('move', 'obstacle_moved', None, {'from': old, 'to': obs.position})

    # -------------------------
    # Draw function
    # -------------------------
    def draw(self, screen, level):
        screen.fill((6,6,20))

        # draw food
        for f in self.food_agents:
            fx = f.position[0]*CELL_SIZE + CELL_SIZE//2
            fy = f.position[1]*CELL_SIZE + CELL_SIZE//2
            base = CELL_SIZE//2 - 4
            pulse = int((1 + 0.5 * (1 + math.sin(self.pulse_offset))) * (FOOD_PULSE_AMPLITUDE/2))
            size = max(6, base + pulse)
            color = (255,255,0) if f.type=='normal' else (0,255,255) if f.type=='bonus' else (255,0,255)
            pygame.draw.circle(screen, color, (fx, fy), size//2)

        # draw obstacles if level >=2
        if level >= 2:
            for o in self.obstacle_agents:
                pygame.draw.rect(screen, (120,120,120), (o.position[0]*CELL_SIZE, o.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # draw human
        for seg in self.human.body:
            pygame.draw.rect(screen, self.human.color, (seg[0]*CELL_SIZE, seg[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # draw alive AI snakes only
        colors = [(0,0,200),(0,0,200),(0,0,200),(0,0,200)]
        for idx, a in enumerate(self.ai_list):
            if a.alive:
                for seg in a.body:
                    pygame.draw.rect(screen, colors[idx%len(colors)], (seg[0]*CELL_SIZE, seg[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # HUD
        y = 6
        txt = self.font.render(f"Level: {level}", True, (255,255,255))
        screen.blit(txt, (8, y))
        y += 22
        scr = self.font.render(f"Human: {self.human.score}", True, self.human.color)
        screen.blit(scr, (8, y))
        y += 18
        for idx, a in enumerate(self.ai_list):
            s = self.font.render(f"AI{idx+1}: {a.score}", True, colors[idx%len(colors)])
            screen.blit(s, (8, y))
            y += 18

    # -------------------------
    # Save event log
    # -------------------------
    def save_event_log(self, path=EVENT_LOG_PATH):
        if not self.event_log:
            return
        with open(path, 'w', newline='', encoding='utf-8') as f:
            keys = ['step','kind','action','agent','pos','extra']
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for ev in self.event_log:
                row = {k: ev.get(k) for k in keys}
                row['pos'] = str(ev.get('pos'))
                row['extra'] = str(ev.get('extra'))
                writer.writerow(row)