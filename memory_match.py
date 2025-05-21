import pygame
import sys
import random
import time
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
CARD_WIDTH = 100
CARD_HEIGHT = 100
CARD_MARGIN = 10
REVEAL_SPEED = 8  # Speed of card flipping animation

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Game states
MENU = 'menu'
GAME = 'game'
GAME_OVER = 'game_over'

# Difficulty levels
EASY = 'easy'
MEDIUM = 'medium'
HARD = 'hard'

# Tech logos to use (we'll use colored rectangles as placeholders)
TECH_LOGOS = ['aws', 'azure', 'docker', 'github', 'python', 'javascript', 'react', 'nodejs']
LOGO_COLORS = {
    'aws': ORANGE,
    'azure': BLUE,
    'docker': LIGHT_BLUE,
    'github': BLACK,
    'python': GREEN,
    'javascript': YELLOW,
    'react': BLUE,
    'nodejs': GREEN
}

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click

class Card:
    def __init__(self, x, y, logo):
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        self.logo = logo
        self.revealed = False
        self.matched = False
        self.animation_progress = 0  # 0 to 100
        self.animating = False
        
    def draw(self, surface):
        if self.matched:
            # Draw matched card (slightly transparent)
            pygame.draw.rect(surface, LOGO_COLORS[self.logo], self.rect, border_radius=5)
            pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)
            font = pygame.font.Font(None, 24)
            text_surface = font.render(self.logo, True, BLACK)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
            return
            
        if self.animating:
            # Draw card animation
            progress = self.animation_progress / 100
            if progress < 0.5:
                # First half of animation (card closing)
                width = CARD_WIDTH * (1 - progress * 2)
                x = self.rect.x + (CARD_WIDTH - width) / 2
                card_rect = pygame.Rect(x, self.rect.y, width, CARD_HEIGHT)
                pygame.draw.rect(surface, GRAY, card_rect, border_radius=5)
                pygame.draw.rect(surface, BLACK, card_rect, 2, border_radius=5)
            else:
                # Second half of animation (card opening)
                width = CARD_WIDTH * ((progress - 0.5) * 2)
                x = self.rect.x + (CARD_WIDTH - width) / 2
                card_rect = pygame.Rect(x, self.rect.y, width, CARD_HEIGHT)
                
                if self.revealed:
                    pygame.draw.rect(surface, LOGO_COLORS[self.logo], card_rect, border_radius=5)
                    if width > CARD_WIDTH * 0.7:  # Only show text when card is mostly open
                        font = pygame.font.Font(None, 24)
                        text_surface = font.render(self.logo, True, BLACK)
                        text_rect = text_surface.get_rect(center=self.rect.center)
                        surface.blit(text_surface, text_rect)
                else:
                    pygame.draw.rect(surface, GRAY, card_rect, border_radius=5)
                
                pygame.draw.rect(surface, BLACK, card_rect, 2, border_radius=5)
        else:
            # Draw static card
            if self.revealed:
                pygame.draw.rect(surface, LOGO_COLORS[self.logo], self.rect, border_radius=5)
                font = pygame.font.Font(None, 24)
                text_surface = font.render(self.logo, True, BLACK)
                text_rect = text_surface.get_rect(center=self.rect.center)
                surface.blit(text_surface, text_rect)
            else:
                pygame.draw.rect(surface, GRAY, self.rect, border_radius=5)
            
            pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)
    
    def animate_flip(self):
        self.animating = True
        self.animation_progress = 0
    
    def update_animation(self):
        if self.animating:
            self.animation_progress += REVEAL_SPEED
            if self.animation_progress >= 100:
                self.animation_progress = 0
                self.animating = False
                
    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click and not self.revealed and not self.matched and not self.animating

class MemoryGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Tech Logo Memory Match')
        self.clock = pygame.time.Clock()
        self.state = MENU
        self.difficulty = EASY
        self.cards = []
        self.first_selection = None
        self.second_selection = None
        self.score = 0
        self.moves = 0
        self.time_left = 0
        self.start_time = 0
        self.game_over = False
        self.match_found = False
        self.wait_time = 0
        
        # Create buttons
        btn_width, btn_height = 200, 50
        center_x = WINDOW_WIDTH // 2 - btn_width // 2
        
        self.easy_btn = Button(center_x, 200, btn_width, btn_height, "Easy", GREEN, (100, 255, 100))
        self.medium_btn = Button(center_x, 280, btn_width, btn_height, "Medium", YELLOW, (255, 255, 100))
        self.hard_btn = Button(center_x, 360, btn_width, btn_height, "Hard", RED, (255, 100, 100))
        self.play_again_btn = Button(center_x, 300, btn_width, btn_height, "Play Again", BLUE, LIGHT_BLUE)
        self.menu_btn = Button(center_x, 380, btn_width, btn_height, "Main Menu", GRAY, (230, 230, 230))
        
    def setup_game(self):
        self.cards = []
        self.first_selection = None
        self.second_selection = None
        self.score = 0
        self.moves = 0
        self.game_over = False
        self.match_found = False
        self.wait_time = 0
        
        # Set up grid based on difficulty
        if self.difficulty == EASY:
            rows, cols = 3, 4
            self.time_left = 60  # 1 minute
        elif self.difficulty == MEDIUM:
            rows, cols = 4, 4
            self.time_left = 90  # 1.5 minutes
        else:  # HARD
            rows, cols = 4, 5
            self.time_left = 120  # 2 minutes
            
        # Calculate card positions
        total_width = cols * (CARD_WIDTH + CARD_MARGIN) - CARD_MARGIN
        total_height = rows * (CARD_HEIGHT + CARD_MARGIN) - CARD_MARGIN
        start_x = (WINDOW_WIDTH - total_width) // 2
        start_y = (WINDOW_HEIGHT - total_height) // 2
        
        # Create pairs of cards
        num_pairs = (rows * cols) // 2
        logos = random.sample(TECH_LOGOS, num_pairs)
        logo_pairs = logos * 2
        random.shuffle(logo_pairs)
        
        # Create card objects
        index = 0
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (CARD_WIDTH + CARD_MARGIN)
                y = start_y + row * (CARD_HEIGHT + CARD_MARGIN)
                self.cards.append(Card(x, y, logo_pairs[index]))
                index += 1
                
        self.start_time = time.time()
        
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_clicked = True
                
        if self.state == MENU:
            self.easy_btn.check_hover(mouse_pos)
            self.medium_btn.check_hover(mouse_pos)
            self.hard_btn.check_hover(mouse_pos)
            
            if self.easy_btn.is_clicked(mouse_pos, mouse_clicked):
                self.difficulty = EASY
                self.setup_game()
                self.state = GAME
            elif self.medium_btn.is_clicked(mouse_pos, mouse_clicked):
                self.difficulty = MEDIUM
                self.setup_game()
                self.state = GAME
            elif self.hard_btn.is_clicked(mouse_pos, mouse_clicked):
                self.difficulty = HARD
                self.setup_game()
                self.state = GAME
                
        elif self.state == GAME:
            # Update timer
            if not self.game_over:
                elapsed = time.time() - self.start_time
                self.time_left = max(0, self.get_initial_time() - int(elapsed))
                
                if self.time_left <= 0:
                    self.game_over = True
                    self.state = GAME_OVER
            
            # Update card animations
            for card in self.cards:
                card.update_animation()
            
            # Check if we need to flip cards back
            if self.wait_time > 0:
                self.wait_time -= 1
                if self.wait_time == 0:
                    if not self.match_found:
                        self.first_selection.animate_flip()
                        self.second_selection.animate_flip()
                        self.first_selection.revealed = False
                        self.second_selection.revealed = False
                    self.first_selection = None
                    self.second_selection = None
            
            # Handle card clicks
            if not self.game_over and self.wait_time == 0 and self.first_selection is None and self.second_selection is None:
                for card in self.cards:
                    if card.is_clicked(mouse_pos, mouse_clicked):
                        card.revealed = True
                        card.animate_flip()
                        self.first_selection = card
                        break
                        
            elif not self.game_over and self.wait_time == 0 and self.first_selection is not None and self.second_selection is None:
                for card in self.cards:
                    if card is not self.first_selection and card.is_clicked(mouse_pos, mouse_clicked):
                        card.revealed = True
                        card.animate_flip()
                        self.second_selection = card
                        self.moves += 1
                        
                        # Check for match
                        if self.first_selection.logo == self.second_selection.logo:
                            self.match_found = True
                            self.score += 1
                            self.first_selection.matched = True
                            self.second_selection.matched = True
                        else:
                            self.match_found = False
                            
                        self.wait_time = 60  # Wait about 1 second before flipping back
                        break
            
            # Check if all cards are matched
            all_matched = all(card.matched for card in self.cards)
            if all_matched:
                self.game_over = True
                self.state = GAME_OVER
                
        elif self.state == GAME_OVER:
            self.play_again_btn.check_hover(mouse_pos)
            self.menu_btn.check_hover(mouse_pos)
            
            if self.play_again_btn.is_clicked(mouse_pos, mouse_clicked):
                self.setup_game()
                self.state = GAME
            elif self.menu_btn.is_clicked(mouse_pos, mouse_clicked):
                self.state = MENU
    
    def get_initial_time(self):
        if self.difficulty == EASY:
            return 60
        elif self.difficulty == MEDIUM:
            return 90
        else:  # HARD
            return 120
                
    def draw(self):
        self.screen.fill(WHITE)
        
        if self.state == MENU:
            # Draw title
            font = pygame.font.Font(None, 64)
            title = font.render("Tech Logo Memory Match", True, BLACK)
            title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
            self.screen.blit(title, title_rect)
            
            # Draw subtitle
            font = pygame.font.Font(None, 32)
            subtitle = font.render("Select Difficulty", True, BLACK)
            subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH//2, 150))
            self.screen.blit(subtitle, subtitle_rect)
            
            # Draw buttons
            self.easy_btn.draw(self.screen)
            self.medium_btn.draw(self.screen)
            self.hard_btn.draw(self.screen)
            
        elif self.state == GAME:
            # Draw cards
            for card in self.cards:
                card.draw(self.screen)
                
            # Draw score and moves
            font = pygame.font.Font(None, 32)
            score_text = font.render(f"Matches: {self.score}", True, BLACK)
            moves_text = font.render(f"Moves: {self.moves}", True, BLACK)
            self.screen.blit(score_text, (20, 20))
            self.screen.blit(moves_text, (20, 60))
            
            # Draw timer
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            timer_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, BLACK)
            self.screen.blit(timer_text, (WINDOW_WIDTH - 150, 20))
            
        elif self.state == GAME_OVER:
            # Draw game over screen
            font = pygame.font.Font(None, 64)
            if all(card.matched for card in self.cards):
                result_text = "You Win!"
                color = GREEN
            else:
                result_text = "Time's Up!"
                color = RED
                
            result = font.render(result_text, True, color)
            result_rect = result.get_rect(center=(WINDOW_WIDTH//2, 100))
            self.screen.blit(result, result_rect)
            
            # Draw stats
            font = pygame.font.Font(None, 32)
            stats_text = [
                f"Matches: {self.score}",
                f"Moves: {self.moves}",
                f"Difficulty: {self.difficulty.capitalize()}"
            ]
            
            for i, text in enumerate(stats_text):
                rendered = font.render(text, True, BLACK)
                self.screen.blit(rendered, (WINDOW_WIDTH//2 - 100, 180 + i*40))
                
            # Draw buttons
            self.play_again_btn.draw(self.screen)
            self.menu_btn.draw(self.screen)
            
        pygame.display.flip()
        
    def run(self):
        while True:
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = MemoryGame()
    game.run()
