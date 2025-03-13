# Chess Player AI

A command-line chess program that lets you play against the computer.

## Features

- Play as white or black
- Three difficulty levels: easy, medium, and hard
- ASCII board display in the console
- Support for standard chess notation (both UCI format like 'e2e4' and algebraic notation like 'Nf3')
- Game commands: help, undo, restart, show legal moves, and quit
- Optional Stockfish integration for stronger computer play

## Requirements

- Python 3.6 or higher
- python-chess library
- IPython (for display capabilities)

## Installation

1. Install the required dependencies:

```
pip install -r requirements.txt
```

2. (Optional) For stronger computer play, download Stockfish:
   - Download from [Stockfish's official site](https://stockfishchess.org/download/)
   - Create a 'stockfish' folder in the same directory as the script
   - Place the appropriate Stockfish executable in the folder based on your OS:
     - Windows: `stockfish/stockfish-windows-x86-64-avx2.exe`
     - Linux: `stockfish/stockfish-ubuntu-x86-64-avx2`
     - macOS: `stockfish/stockfish-macos-x86-64-modern`

## How to Play

Run the game with:

```
python chess_player_ai.py
```

Follow the prompts to:
1. Choose your color (white or black)
2. Select difficulty level (easy, medium, or hard)

### Game Commands

During play, you can use these commands:
- Enter moves in UCI format (e.g., 'e2e4') or standard algebraic notation (e.g., 'Nf3')
- Type 'help' to see available commands
- Type 'moves' to see all legal moves
- Type 'undo' to take back the last move
- Type 'restart' to start a new game
- Type 'quit' to exit the game

## Notes

- If Stockfish is not available, the computer will make random legal moves
- The game displays the board after each move and shows the move history
- Special chess conditions like checkmate, stalemate, and check are detected and displayed
