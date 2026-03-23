# 2048 Game

2048 with AI. The AI uses Expectimax to play automatically.

## Setup

You need Python 3.10 or newer. No pip packages required.

```bash
git clone <repo-url>
cd 2048-game
python main.py
```

## Usage

When you run `main.py` it asks you to pick a mode:

- **m** -- play yourself with w/a/s/d
- **a** -- watch the AI play (Expectimax, depth 3)

To compare the different algorithms against each other:

```bash
python compare_algorithms.py
```

This runs Random, Greedy, MCTS, Minimax, and Expectimax on the same seed and prints the results.

## Project layout

The AI and the game engine live in two separate folders: `ai/` and `engine/`. Both were implemented by the group but kept completely independent. The AI borrows no code from the engine or anywhere else. Everything inside `ai/` was written from scratch. The engine handles the game rules, board state, and tile spawning. The AI only reads the board through the engine's public interface and decides which move to make.
