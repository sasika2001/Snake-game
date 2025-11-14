import math
import pygame
import random
from core.config import GRID_SIZE, CELL_SIZE, FOOD_PULSE_SPEED, FOOD_PULSE_AMPLITUDE, FONT_NAME

def load_sound(path):
    try: return pygame.mixer.Sound(path)
    except Exception: return None

class Environment:
    def __init__(self, human, ai_list):
        self.human = human
        self.ai_list = ai_list
        self.food_positions = []
        self.food_types = {}
        self.obstacles = []
        self.pulse_offset = 0.0
        self.font = pygame.font.SysFont(FONT_NAME, 18)
        self.eat_sound=load_sound('assets/sounds/eat.wav')
        self.levelup_sound=load_sound('assets/sounds/levelup.wav')
        self.gameover_sound=load_sound('assets/sounds/gameover.wav')
        self.spawn_food(5)

    def spawn_food(self,count=1):
        for _ in range(count):
            while True:
                p=(random.randint(0,GRID_SIZE-1),random.randint(0,GRID_SIZE-1))
                if p not in self.all_occupied():
                    self.food_positions.append(p)
                    r=random.random()
                    if r<0.8: self.food_types[p]='normal'
                    elif r<0.95: self.food_types[p]='bonus'
                    else: self.food_types[p]='poison'
                    break

    def spawn_obstacles(self,count=3):
        added=0; attempts=0
        while added<count and attempts<200:
            p=(random.randint(0,GRID_SIZE-1),random.randint(0,GRID_SIZE-1))
            if p not in self.all_occupied():
                self.obstacles.append(p)
                added+=1
            attempts+=1

    def all_occupied(self):
        occ=self.human.body[:]
        for a in self.ai_list: occ+=a.body
        occ+=self.food_positions
        occ+=self.obstacles
        return occ

    def step(self,level):
        self.pulse_offset+=1.0/FOOD_PULSE_SPEED
        for ai in self.ai_list:
            ai.sensing_range=min(GRID_SIZE, ai.sensing_range + (1 if level>1 else 0))
            ai.smartness=1+max(0,level-1)
        self.human.step(self.food_positions,self.food_types,self.obstacles)
        for ai in self.ai_list:
            ai.step(self.food_positions,self.food_types,[self.human]+[x for x in self.ai_list if x is not ai],self.obstacles)
        while len(self.food_positions)<5:
            self.spawn_food(1)
        if level>=3:
            for i,(x,y) in enumerate(self.obstacles):
                if random.random()<0.07:
                    nx=max(0,min(GRID_SIZE-1,x+random.choice([-1,0,1])))
                    ny=max(0,min(GRID_SIZE-1,y+random.choice([-1,0,1])))
                    if (nx,ny) not in self.all_occupied(): self.obstacles[i]=(nx,ny)

    def draw(self,screen,level):
        screen.fill((6,6,20))
        for p in list(self.food_positions):
            fx=p[0]*CELL_SIZE+CELL_SIZE//2
            fy=p[1]*CELL_SIZE+CELL_SIZE//2
            base=CELL_SIZE//2-4
            pulse = int((1 + 0.5 * (1 + math.sin(self.pulse_offset))) * (FOOD_PULSE_AMPLITUDE / 2))
            size=max(6,base+pulse)
            color=(255,255,0)
            ftype=self.food_types.get(p,'normal')
            if ftype=='bonus': color=(0,255,255)
            if ftype=='poison': color=(255,0,255)
            pygame.draw.circle(screen,color,(fx,fy),size//2)
        if level>=2:
            for o in self.obstacles:
                pygame.draw.rect(screen,(120,120,120),(o[0]*CELL_SIZE,o[1]*CELL_SIZE,CELL_SIZE,CELL_SIZE))
        for seg in self.human.body:
            pygame.draw.rect(screen,self.human.color,(seg[0]*CELL_SIZE,seg[1]*CELL_SIZE,CELL_SIZE,CELL_SIZE))
        colors=[(200,0,0),(0,0,200),(200,0,200),(0,200,200)]
        for idx,a in enumerate(self.ai_list):
            for seg in a.body:
                pygame.draw.rect(screen,colors[idx%len(colors)],(seg[0]*CELL_SIZE,seg[1]*CELL_SIZE,CELL_SIZE,CELL_SIZE))
        y=6
        txt=self.font.render(f"Level: {level}",True,(255,255,255))
        screen.blit(txt,(8,y))
        y+=22
        scr=self.font.render(f"Human: {self.human.score}",True,self.human.color)
        screen.blit(scr,(8,y))
        y+=18
        for idx,a in enumerate(self.ai_list):
            s=self.font.render(f"AI{idx+1}: {a.score}",True,colors[idx%len(colors)])
            screen.blit(s,(8,y))
            y+=18
