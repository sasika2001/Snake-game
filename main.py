# main.py
import pygame, sys
from core.config import WINDOW_WIDTH, WINDOW_HEIGHT, BASE_FPS, FPS_INCREMENT, LEVEL_UP_SCORE, FONT_NAME, EVENT_LOG_PATH
from agents.human_agent import HumanAgent
from agents.cognitive_ai_agent import CognitiveAIAgent
from game.environment import Environment

pygame.init()
try:
    pygame.mixer.init()
except Exception:
    pass

def safe_play(sound):
    if sound:
        try:
            sound.play()
        except:
            pass

def draw_text_center(screen, text, font, color, y):
    txt = font.render(text, True, color)
    screen.blit(txt, (WINDOW_WIDTH//2 - txt.get_width()//2, y))

def start_menu(screen):
    clock = pygame.time.Clock()
    font_large = pygame.font.SysFont(FONT_NAME, 50)
    font_medium = pygame.font.SysFont(FONT_NAME, 36)

    difficulty_levels = ['Easy', 'Medium', 'Hard']
    ai_options = [1, 2, 3]
    selected_difficulty = 0
    selected_ai = 0
    menu_stage = 0  # 0=difficulty, 1=AI count

    running = True
    while running:
        screen.fill((20, 20, 40))
        y = 100
        draw_text_center(screen, "Snake Arena", font_large, (255,255,0), y)
        y += 100

        if menu_stage == 0:
            draw_text_center(screen, "Select Difficulty:", font_medium, (255,255,255), y)
            y += 50
            for idx, level in enumerate(difficulty_levels):
                color = (255,255,0) if idx == selected_difficulty else (200,200,200)
                draw_text_center(screen, level, font_medium, color, y + idx*40)
        elif menu_stage == 1:
            draw_text_center(screen, "Select Number of AI Agents:", font_medium, (255,255,255), y)
            y += 50
            for idx, num in enumerate(ai_options):
                color = (255,255,0) if idx == selected_ai else (200,200,200)
                draw_text_center(screen, f"{num} AI", font_medium, color, y + idx*40)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if menu_stage == 0:
                        selected_difficulty = (selected_difficulty + 1) % len(difficulty_levels)
                    else:
                        selected_ai = (selected_ai + 1) % len(ai_options)
                if event.key == pygame.K_UP:
                    if menu_stage == 0:
                        selected_difficulty = (selected_difficulty - 1) % len(difficulty_levels)
                    else:
                        selected_ai = (selected_ai - 1) % len(ai_options)
                if event.key == pygame.K_RETURN:
                    if menu_stage == 0:
                        menu_stage = 1
                    else:
                        return difficulty_levels[selected_difficulty], ai_options[selected_ai]

        clock.tick(30)

def game_over_screen(screen, human, ai_list, env):
    clock = pygame.time.Clock()
    font_large = pygame.font.SysFont(FONT_NAME, 50)
    font_medium = pygame.font.SysFont(FONT_NAME, 36)

    while True:
        screen.fill((0,0,0))
        y = 80
        draw_text_center(screen, "Game Over!", font_large, (255,0,0), y)
        y += 80
        draw_text_center(screen, f"Human: {human.score}", font_medium, human.color, y)
        y += 50
        colors = [(200,0,0),(0,0,200),(200,0,200)]
        for idx, a in enumerate(ai_list):
            draw_text_center(screen, f"AI{idx+1}: {a.score}", font_medium, colors[idx%len(colors)], y)
            y += 40
        scores = [(human.score, "Human")] + [(a.score, f"AI{idx+1}") for idx, a in enumerate(ai_list)]
        winner = max(scores, key=lambda x: x[0])
        y += 20
        draw_text_center(screen, f"Winner: {winner[1]}", font_medium, (255,255,0), y)
        y += 80
        draw_text_center(screen, "Press R to Restart or Q to Quit", font_medium, (255,255,255), y)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # restart
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        clock.tick(30)

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Cognitive MAS Snake Arena (Rational + Complex Systems)")

    restart_game = True
    while restart_game:
        difficulty, num_ai = start_menu(screen)

        # set FPS based on difficulty
        fps = BASE_FPS
        if difficulty == 'Easy':
            level_up_score = 10
            fps_increment = 1
        elif difficulty == 'Medium':
            level_up_score = 8
            fps_increment = 2
        else:
            level_up_score = 5
            fps_increment = 3

        # create agents
        human = HumanAgent(0, (5,5))
        ai_list = [CognitiveAIAgent(i+1, (15+i*2,15+i*2)) for i in range(num_ai)]
        env = Environment(human, ai_list, seed=None)

        level = 1
        last_level = 1
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    human.handle_event(event)

            env.step(level)

            # Level up by human + AI scores
            highest = max([human.score] + [a.score for a in ai_list])
            target_level = 1 + highest // level_up_score
            if target_level > level:
                level += 1  # step by step
                fps += fps_increment
                safe_play(env.levelup_sound)
                if level == 2:
                    env.spawn_obstacles(2)
                elif level == 3:
                    env.spawn_obstacles(3)
                    env.spawn_food(1)
                elif level >= 4:
                    env.spawn_obstacles(4)
                    env.spawn_food(2)

            # Draw environment
            env.draw(screen, level)
            pygame.display.flip()

            # -------------------------
            # Game over logic
            # -------------------------
            alive_ai = [a for a in ai_list if a.alive]
            total_alive = [human] + alive_ai

            if not human.alive:
                running = False
            elif len(total_alive) == 2 and len(alive_ai) == 0:
                running = False  # Only 2 snakes and AI dead
            # Dead AI snakes are invisible but game continues if more than 2 snakes

            clock.tick(fps)

        restart_game = game_over_screen(screen, human, ai_list, env)
        env.save_event_log(EVENT_LOG_PATH)

if __name__ == "__main__":
    main()