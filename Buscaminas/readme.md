# Minesweeper

## 📜 Description
Minesweeper is a classic puzzle game where the goal is to clear a board without detonating hidden mines.  
Players uncover tiles and use logic to deduce where the mines are located.  
The game ends when all non-mine tiles are revealed or if a mine is triggered.

## 🎮 How It Works
1. **Board Generation**  
   - A grid of tiles is created with a set number of hidden mines placed randomly.
2. **Revealing Tiles**  
   - Clicking a tile reveals it.  
   - If the tile contains a mine → 💥 Game Over.  
   - If not, it shows a number indicating how many mines are adjacent (including diagonals).
3. **Flagging Mines**  
   - Right-click a tile to place or remove a flag, marking suspected mines.
4. **Winning Condition**  
   - The player wins when all non-mine tiles are uncovered.

## 🛠️ Technologies Used
- **C** → Structure of the board, game logic, mine generation and user interaction handling.
- **SDL2 Library** → Interface.

## 🚀 Features
- Randomized mine placement.
- Dynamic number calculation for each tile.
- Flag system to mark suspected mines.
- Win/Lose game state detection.

**Enjoy playing and challenge your logic skills!**
