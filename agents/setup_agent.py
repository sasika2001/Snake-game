# agents/setup_agent.py
import pygame
from core.config import FONT_NAME, WINDOW_WIDTH, WINDOW_HEIGHT

class SetupAgent:
    def __init__(self):
        self.difficulty = None
        self.num_ai_agents = None
        self.selected = False

        self.font_title = pygame.font.SysFont(FONT_NAME, 48, bold=True)
        self.font_buttons = pygame.font.SysFont(FONT_NAME, 28, bold=True)
        self.font_instructions = pygame.font.SysFont(FONT_NAME, 20)

        # Button definitions: (text, rect)
        self.buttons = {
            "Easy": pygame.Rect(WINDOW_WIDTH//2-180, 200, 140, 60),
            "Medium": pygame.Rect(WINDOW_WIDTH//2-70, 200, 140, 60),
            "Hard": pygame.Rect(WINDOW_WIDTH//2+40, 200, 140, 60),
            "AI1": pygame.Rect(WINDOW_WIDTH//2-130, 320, 100, 60),
            "AI2": pygame.Rect(WINDOW_WIDTH//2-20, 320, 100, 60),
            "AI3": pygame.Rect(WINDOW_WIDTH//2+90, 320, 100, 60),
        }

    def display_menu(self, screen):
        # Gradient background
        for i in range(WINDOW_HEIGHT):
            color = (30 + i//20, 30 + i//20, 60 + i//5)
            pygame.draw.line(screen, color, (0,i), (WINDOW_WIDTH,i))

        # Title
        title = self.font_title.render("SNAKE ARENA", True, (255, 200, 0))
        subtitle = self.font_buttons.render("Select Difficulty & AI Count", True, (255,255,255))
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 50))
        screen.blit(subtitle, (WINDOW_WIDTH//2 - subtitle.get_width()//2, 120))

        # Draw buttons with hover effect
        mouse_pos = pygame.mouse.get_pos()
        for text, rect in self.buttons.items():
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255,140,0), rect, border_radius=10)
            else:
                pygame.draw.rect(screen, (80, 80, 200), rect, border_radius=10)
            label = self.font_buttons.render(text, True, (255,255,255))
            screen.blit(label, (rect.x + rect.width//2 - label.get_width()//2, rect.y + rect.height//2 - label.get_height()//2))

        # Show selected choices
        y = 420
        if self.difficulty:
            txt = self.font_buttons.render(f"Difficulty: {self.difficulty}", True, (255,255,0))
            screen.blit(txt, (WINDOW_WIDTH//2 - txt.get_width()//2, y))
            y += 50
        if self.num_ai_agents:
            txt = self.font_buttons.render(f"AI Agents: {self.num_ai_agents}", True, (255,255,0))
            screen.blit(txt, (WINDOW_WIDTH//2 - txt.get_width()//2, y))
            y += 50

        # Instructions
        instr = self.font_instructions.render("Click buttons to select options, then start the game", True, (200,200,200))
        screen.blit(instr, (WINDOW_WIDTH//2 - instr.get_width()//2, WINDOW_HEIGHT - 50))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for text, rect in self.buttons.items():
                if rect.collidepoint(pos):
                    if text in ["Easy", "Medium", "Hard"]:
                        self.difficulty = text
                    elif text in ["AI1","AI2","AI3"]:
                        self.num_ai_agents = int(text[-1])
        if self.difficulty and self.num_ai_agents:
            self.selected = True

    def get_settings(self):
        return self.difficulty, self.num_ai_agents
