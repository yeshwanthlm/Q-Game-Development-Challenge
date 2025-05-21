# Building a Tech Logo Memory Match Game with Pygame

Memory games are not only fun but also help improve cognitive skills like concentration and short-term memory. In this blog post, I'll walk you through how I built a tech-themed memory matching card game using Python and Pygame.

## Project Overview

The Tech Logo Memory Match Game is a classic card-matching game where players flip cards to find matching pairs. What makes this version special is that it features logos from popular tech companies, making it both entertaining and educational for tech enthusiasts.

![Game Preview](assets/game_preview.png)

## Key Features

- **Tech-themed cards**: Featuring logos from companies like AWS, Azure, Docker, GitHub, and more
- **Multiple difficulty levels**: Easy (3x4 grid), Medium (4x4 grid), and Hard (4x5 grid)
- **Countdown timer**: Adding excitement and challenge
- **Score tracking**: Keeping count of moves and completion time
- **Smooth animations**: Card flipping animations for better user experience

## The Development Process

### 1. Setting Up the Project

I started by setting up the basic structure of the project:

```python
import pygame
import random
import time
import sys

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tech Logo Memory Match")
```

### 2. Creating the Card Class

The Card class is the foundation of the game, handling the state and behavior of each card:

```python
class Card:
    def __init__(self, x, y, width, height, logo_img, back_img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.logo_img = logo_img
        self.back_img = back_img
        self.is_flipped = False
        self.is_matched = False
        
    def draw(self, screen):
        if self.is_flipped or self.is_matched:
            screen.blit(self.logo_img, (self.x, self.y))
        else:
            screen.blit(self.back_img, (self.x, self.y))
    
    def is_clicked(self, mouse_pos):
        return (self.x <= mouse_pos[0] <= self.x + self.width and
                self.y <= mouse_pos[1] <= self.y + self.height)
```

### 3. Implementing Game Logic

The core game logic involves:
- Shuffling and distributing cards
- Handling card flips
- Checking for matches
- Managing the timer and game state

```python
def check_for_match(flipped_cards):
    if len(flipped_cards) == 2:
        if flipped_cards[0].logo_img == flipped_cards[1].logo_img:
            flipped_cards[0].is_matched = True
            flipped_cards[1].is_matched = True
            return True
    return False
```

### 4. Creating the User Interface

A clean, intuitive UI is crucial for a good gaming experience:

```python
def draw_ui(screen, time_left, moves, difficulty):
    # Draw background
    screen.fill((40, 44, 52))
    
    # Draw timer
    font = pygame.font.SysFont('Arial', 24)
    timer_text = font.render(f"Time: {time_left}s", True, (255, 255, 255))
    screen.blit(timer_text, (20, 20))
    
    # Draw moves counter
    moves_text = font.render(f"Moves: {moves}", True, (255, 255, 255))
    screen.blit(moves_text, (WIDTH - 120, 20))
    
    # Draw difficulty
    diff_text = font.render(f"Difficulty: {difficulty}", True, (255, 255, 255))
    screen.blit(diff_text, (WIDTH // 2 - 80, 20))
```

### 5. Adding Difficulty Levels

Different difficulty levels keep the game challenging and engaging:

```python
def setup_game(difficulty):
    if difficulty == "Easy":
        rows, cols = 3, 4
        time_limit = 60
    elif difficulty == "Medium":
        rows, cols = 4, 4
        time_limit = 90
    else:  # Hard
        rows, cols = 4, 5
        time_limit = 120
        
    # Create and return the game board
    return create_board(rows, cols), time_limit
```

### 6. Implementing Animations

Smooth animations enhance the gaming experience:

```python
def flip_animation(card, screen, clock, frames=10):
    original_width = card.width
    
    for i in range(frames):
        # Calculate width for this frame
        current_width = original_width * (frames - i) / frames
        
        # Clear the card area
        pygame.draw.rect(screen, (40, 44, 52), 
                        (card.x, card.y, original_width, card.height))
        
        # Draw the card with the current width
        scaled_img = pygame.transform.scale(
            card.back_img if not card.is_flipped else card.logo_img,
            (int(current_width), card.height)
        )
        screen.blit(scaled_img, (card.x + (original_width - current_width)/2, card.y))
        
        pygame.display.update()
        clock.tick(60)
```

## Challenges and Solutions

### Challenge 1: Card Matching Logic

One of the initial challenges was implementing the card matching logic correctly. I needed to ensure that:
- Only two cards could be flipped at once
- Matched cards stayed face up
- Unmatched cards flipped back after a short delay

The solution was to use a list to track flipped cards and implement a state machine to manage the game flow.

### Challenge 2: Responsive Layout

Making the game look good on different screen sizes was another challenge. I solved this by calculating card positions dynamically based on the screen dimensions and the number of cards.

### Challenge 3: Performance Optimization

With animations and multiple images, performance could be an issue. I optimized by:
- Pre-loading all images at startup
- Using efficient drawing techniques
- Limiting unnecessary screen updates

## Lessons Learned

Building this game taught me several valuable lessons:

1. **Planning is crucial**: Having a clear structure before coding saved time and reduced bugs
2. **User experience matters**: Small details like animations and clear UI make a big difference
3. **Testing is essential**: Regular testing with different scenarios helped catch issues early

## Future Improvements

There are several ways I plan to enhance this game in the future:

1. Add sound effects and background music
2. Implement a high score system
3. Create custom themes beyond tech logos
4. Add multiplayer functionality
5. Optimize for mobile devices

## Conclusion

Creating this Tech Logo Memory Match Game was both fun and educational. Pygame provides a great framework for building simple games, and the project helped me improve my Python skills while creating something enjoyable.

If you're interested in trying the game yourself or contributing to its development, check out the [GitHub repository](https://github.com/yourusername/tech-logo-memory-match).

Happy coding and happy matching!

---

*Note: Don't forget to replace the GitHub repository link with your actual repository URL once you've created it.*
