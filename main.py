# main.py
import pygame, sys
from core.config import WINDOW_WIDTH, WINDOW_HEIGHT, BASE_FPS, FPS_INCREMENT, LEVEL_UP_SCORE, FONT_NAME, BUTTERFLY_MODE, EVENT_LOG_PATH
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

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Cognitive MAS Snake Arena (Rational + Complex Systems)")
    clock = pygame.time.Clock()

    # -------------------------
    # Create agents
    # -------------------------
    human = HumanAgent(0, (5,5))
    ai_list = [
        CognitiveAIAgent(1, (15,15)),
        CognitiveAIAgent(2, (10,10))
    ]
    env = Environment(human, ai_list, seed=None)

    level = 1
    fps = BASE_FPS
    font_large = pygame.font.SysFont(FONT_NAME, 36)
    last_level = level
    running = True

    while running:
        # -------------------------
        # Event handling
        # -------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                human.handle_event(event)

        # -------------------------
        # Step environment
        # -------------------------
        env.step(level)

        # -------------------------
        # Level up by highest score
        # -------------------------
        highest = max([human.score] + [a.score for a in ai_list])
        target_level = 1 + highest // LEVEL_UP_SCORE
        if target_level > level:
            level = target_level
            fps += FPS_INCREMENT
            safe_play(env.levelup_sound)

            # Dynamic spawning based on level
            if level == 2:
                env.spawn_obstacles(4)
            elif level == 3:
                env.spawn_obstacles(6)
                env.spawn_food(2)
            elif level >= 4:
                env.spawn_obstacles(8)
                env.spawn_food(3)

        # -------------------------
        # Draw everything
        # -------------------------
        env.draw(screen, level)
        if level != last_level:
            txt = font_large.render(f"Level {level}", True, (255,255,0))
            screen.blit(txt, (WINDOW_WIDTH//2 - txt.get_width()//2, 20))
            last_level = level

        pygame.display.flip()

        # -------------------------
        # End game if human dead
        # -------------------------
        if not human.alive:
            running = False
            break

        clock.tick(fps)

    # -------------------------
    # Game Over - Display Scores
    # -------------------------
    screen.fill((0,0,0))
    y = 50
    title = font_large.render("Game Over! Final Scores:", True, (255,255,255))
    screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, y))
    y += 50

    # Human score
    scr = font_large.render(f"Human: {human.score}", True, human.color)
    screen.blit(scr, (WINDOW_WIDTH//2 - scr.get_width()//2, y))
    y += 40

    # AI scores
    colors = [(200,0,0),(0,0,200),(200,0,200),(0,200,200)]
    for idx, a in enumerate(ai_list):
        s = font_large.render(f"AI{idx+1}: {a.score}", True, colors[idx%len(colors)])
        screen.blit(s, (WINDOW_WIDTH//2 - s.get_width()//2, y))
        y += 40

    # Determine winner
    scores = [(human.score, "Human")] + [(a.score, f"AI{idx+1}") for idx, a in enumerate(ai_list)]
    winner = max(scores, key=lambda x: x[0])
    winner_txt = font_large.render(f"Winner: {winner[1]}", True, (255,255,0))
    screen.blit(winner_txt, (WINDOW_WIDTH//2 - winner_txt.get_width()//2, y+20))

    pygame.display.flip()
    safe_play(env.gameover_sound)
    pygame.time.delay(5000)

    # Save event log
    env.save_event_log(EVENT_LOG_PATH)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
