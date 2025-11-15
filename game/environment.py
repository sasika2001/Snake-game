# game/environment.py
import pygame, random, math, csv, os
from core.config import GRID_SIZE, CELL_SIZE, FOOD_PULSE_SPEED, FOOD_PULSE_AMPLITUDE, FONT_NAME, BUTTERFLY_MODE, BUTTERFLY_STEP, EVENT_LOG_PATH

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
        self.food_positions = []
        self.food_types = {}
        self.obstacles = []
        self.pulse_offset = 0.0
        self.font = pygame.font.SysFont(FONT_NAME, 18)
        self.eat_sound = load_sound('assets/sounds/eat.wav')
        self.levelup_sound = load_sound('assets/sounds/levelup.wav')
        self.gameover_sound = load_sound('assets/sounds/gameover.wav')
        # message bus / shared dangers
        self.shared_dangers = set()
        # event log list of tuples
        self.event_log = []
        self.step_count = 0
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        self.spawn_food(5)
        # ensure events directory exists
        if not os.path.exists('events'):
            os.makedirs('events')

    def log_event(self, kind, action, agent_id, pos=None, extra=None):
        # simple structured event: step,kind,action,agent,pos,extra
        self.event_log.append({'step': self.step_count, 'kind': kind, 'action': action, 'agent': agent_id, 'pos': pos, 'extra': extra})

    def broadcast(self, msg):
        # handle broadcast messages (simple)
        if msg['type'] == 'danger':
            self.shared_dangers.add(tuple(msg['pos']))
            # log broadcast
            self.log_event('broadcast', 'danger_broadcast', msg.get('from'), tuple(msg.get('pos')))

    def spawn_food(self, count=1):
        for _ in range(count):
            tries = 0
            while True:
                p = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
                if p not in self.all_occupied():
                    self.food_positions.append(p)
                    r = random.random()
                    if r < 0.80:
                        self.food_types[p] = 'normal'
                    elif r < 0.95:
                        self.food_types[p] = 'bonus'
                    else:
                        self.food_types[p] = 'poison'
                    self.log_event('spawn','food_spawned', None, p, extra={'type': self.food_types[p]})
                    break
                tries += 1
                if tries > 200:
                    break

    def spawn_obstacles(self, count=3):
        added = 0; attempts = 0
        while added < count and attempts < 300:
            p = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
            if p not in self.all_occupied():
                self.obstacles.append(p)
                added += 1
                self.log_event('spawn','obstacle_spawned', None, p)
            attempts += 1

    def all_occupied(self):
        occ = []
        occ += list(self.human.body)
        for a in self.ai_list:
            occ += list(a.body)
        occ += list(self.food_positions)
        occ += self.obstacles
        return occ

    def step(self, level):
        self.step_count += 1
        self.pulse_offset += 1.0 / FOOD_PULSE_SPEED

        # optional butterfly perturbation: small random change at predetermined step
        if BUTTERFLY_MODE and self.step_count == BUTTERFLY_STEP:
            # tiny perturbation: move one food spawn by one cell
            if self.food_positions:
                i = random.randrange(len(self.food_positions))
                old = self.food_positions[i]
                new = (max(0, min(GRID_SIZE-1, old[0] + random.choice([-1,0,1]))),
                       max(0, min(GRID_SIZE-1, old[1] + random.choice([-1,0,1]))))
                self.food_positions[i] = new
                # update type mapping
                t = self.food_types.pop(old, 'normal')
                self.food_types[new] = t
                self.log_event('butterfly', 'food_perturb', None, {'from': old, 'to': new})

        # adjust AI cognitive params by level
        for ai in self.ai_list:
            ai.sensing_range = min(GRID_SIZE, ai.sensing_range + (1 if level > 1 else 0))
            ai.smartness = 1 + max(0, level - 1)

        # human acts
        self.human.step(self.food_positions, self.food_types, self.obstacles)
        # AI acts
        for ai in self.ai_list:
            events = ai.step(self.food_positions, self.food_types, [self.human] + [x for x in self.ai_list if x is not ai], self.obstacles, self)
            for e in events:
                if e[0] == 'ate':
                    # environment handles removal and sound in centralized way
                    pass

        # centralized eat handling and sound (ensures sound played once)
        eaten_positions = []
        for agent in [self.human] + self.ai_list:
            head = agent.body[0] if agent.alive else None
            if head and head in self.food_positions:
                eaten_positions.append((agent.id, head, self.food_types.get(head, 'normal')))
        for agent_id, pos, ftype in eaten_positions:
            # remove food and play sound
            if pos in self.food_positions:
                self.food_positions.remove(pos)
            if pos in self.food_types:
                self.food_types.pop(pos, None)
            if self.eat_sound:
                try: self.eat_sound.play()
                except: pass
            self.log_event('eat', 'food_eaten', agent_id, pos, extra={'type': ftype})

        # respawn food if low
        while len(self.food_positions) < 5:
            self.spawn_food(1)

        # move obstacles at high level -> increases complexity
        if level >= 3:
            for i, (x, y) in enumerate(self.obstacles):
                if random.random() < 0.07:
                    nx = max(0, min(GRID_SIZE-1, x + random.choice([-1,0,1])))
                    ny = max(0, min(GRID_SIZE-1, y + random.choice([-1,0,1])))
                    if (nx, ny) not in self.all_occupied():
                        old = self.obstacles[i]
                        self.obstacles[i] = (nx, ny)
                        self.log_event('move', 'obstacle_moved', None, {'from': old, 'to': (nx, ny)})

    def draw(self, screen, level):
        screen.fill((6,6,20))
        for p in list(self.food_positions):
            fx = p[0]*CELL_SIZE + CELL_SIZE//2
            fy = p[1]*CELL_SIZE + CELL_SIZE//2
            base = CELL_SIZE//2 - 4
            pulse = int((1 + 0.5 * (1 + math.sin(self.pulse_offset))) * (FOOD_PULSE_AMPLITUDE/2))
            size = max(6, base + pulse)
            color = (255,255,0)
            ftype = self.food_types.get(p,'normal')
            if ftype == 'bonus': color = (0,255,255)
            if ftype == 'poison': color = (255,0,255)
            pygame.draw.circle(screen, color, (fx, fy), size//2)
        if level >= 2:
            for o in self.obstacles:
                pygame.draw.rect(screen, (120,120,120), (o[0]*CELL_SIZE, o[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for seg in self.human.body:
            pygame.draw.rect(screen, self.human.color, (seg[0]*CELL_SIZE, seg[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        colors = [(200,0,0),(0,0,200),(200,0,200),(0,200,200)]
        for idx, a in enumerate(self.ai_list):
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

    def save_event_log(self, path=EVENT_LOG_PATH):
        # write event_log to CSV for analysis (append if exists)
        if not self.event_log:
            return
        with open(path, 'w', newline='', encoding='utf-8') as f:
            keys = ['step','kind','action','agent','pos','extra']
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for ev in self.event_log:
                # serialize pos and extra to simple strings
                row = {k: ev.get(k) for k in keys}
                row['pos'] = str(ev.get('pos'))
                row['extra'] = str(ev.get('extra'))
                writer.writerow(row)
