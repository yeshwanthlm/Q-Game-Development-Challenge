# Tech Logo Memory Match Game

![Memory Match Game](assets/game_preview.png)

A memory matching card game built with Pygame featuring iconic tech logos. Test your memory by matching pairs of tech company logos against the clock!

## 🎮 Features

- **Multiple Difficulty Levels**: Choose between Easy, Medium, and Hard
- **Countdown Timer**: Race against time to find all matches
- **Smooth Animations**: Enjoy fluid card flip animations
- **Tech-Themed Cards**: Match logos from popular tech companies (AWS, Azure, Docker, GitHub, etc.)
- **Score Tracking**: Monitor your moves and completion time

## 🚀 How to Play

1. Clone this repository
2. Install the requirements
3. Run the game: `python memory_match.py`
4. Select a difficulty level
5. Click on cards to flip them and find matching pairs
6. Match all pairs before the timer runs out to win!

## 📋 Requirements

- Python 3.x
- Pygame library

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/tech-logo-memory-match.git
cd tech-logo-memory-match

# Install pygame if you don't have it
pip install pygame

# Run the game
python memory_match.py
```

## 🎯 Game Controls

- **Mouse**: Click to select cards and navigate menus
- **ESC**: Pause game / Return to main menu

## 🏆 Difficulty Levels

| Level  | Grid Size | Pairs | Time Limit |
|--------|-----------|-------|------------|
| Easy   | 3x4       | 6     | 60 seconds |
| Medium | 4x4       | 8     | 90 seconds |
| Hard   | 4x5       | 10    | 120 seconds |

## 📷 Screenshots

![Main Menu](assets/main_menu.png)
![Gameplay](assets/gameplay.png)
![Victory Screen](assets/victory.png)

## 🛠️ Project Structure

```
tech-logo-memory-match/
├── memory_match.py     # Main game file
├── assets/             # Game assets directory
│   ├── images/         # Card images and logos
│   ├── fonts/          # Game fonts
│   └── sounds/         # Game sound effects
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
