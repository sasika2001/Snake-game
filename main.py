import pygame, sys
from core.config import WINDOW_WIDTH, WINDOW_HEIGHT, BASE_FPS, FPS_INCREMENT, LEVEL_UP_SCORE, FONT_NAME
from agents.human_agent import HumanAgent
from agents.cognitive_ai_agent import CognitiveAIAgent
from game.environment import Environment

pygame.init()
try: pygame.mixer.init()
except: pass

def safe_play(sound):
    if sound:
        try: sound.play()
        except: pass

def main():
    screen=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("Cognitive MAS Snake Arena")
    clock=pygame.time.Clock()
    human=HumanAgent(0,(5,5))
    ai_list=[CognitiveAIAgent(1,(15,15)),CognitiveAIAgent(2,(10,10))]
    env=Environment(human,ai_list)
    level=1; fps=BASE_FPS
    font_large=pygame.font.SysFont(FONT_NAME,36)
    running=True; last_level=level
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT: running=False
            else: human.handle_event(event)
        env.step(level)
        highest=max([human.score]+[a.score for a in ai_list])
        target_level=1+highest//LEVEL_UP_SCORE
        if target_level>level:
            level=target_level; fps+=FPS_INCREMENT
            safe_play(env.levelup_sound)
            if level==2: env.spawn_obstacles(4)
            elif level==3: env.spawn_obstacles(6)
            elif level>=4: env.spawn_obstacles(8); env.spawn_food(2)
        env.draw(screen,level)
        if level!=last_level:
            txt=font_large.render(f"Level {level}",True,(255,255,0))
            screen.blit(txt,(WINDOW_WIDTH//2-txt.get_width()//2,20))
            last_level=level
        pygame.display.flip()
        if not human.alive:
            safe_play(env.gameover_sound)
            screen.fill((0,0,0))
            txt=font_large.render("AI Snakes Win!",True,(255,80,80))
            screen.blit(txt,(WINDOW_WIDTH//2-txt.get_width()//2,WINDOW_HEIGHT//2-txt.get_height()//2))
            pygame.display.flip()
            pygame.time.delay(2500)
            running=False
        elif all(not a.alive for a in ai_list):
            safe_play(env.eat_sound)
            screen.fill((0,0,0))
            txt=font_large.render("Human Wins!",True,(80,255,80))
            screen.blit(txt,(WINDOW_WIDTH//2-txt.get_width()//2,WINDOW_HEIGHT//2-txt.get_height()//2))
            pygame.display.flip()
            pygame.time.delay(2500)
            running=False
        clock.tick(fps)
    pygame.quit(); sys.exit()

if __name__=="__main__":
    main()
