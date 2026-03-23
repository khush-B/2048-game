# 2048 AI Game

A terminal-based 2048 game with an AI player powered by **Expectimax search**.

---

## Requirements

- **Python 3.10+** (standard library only — no external packages needed)

## Installation & Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd 2048-game

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. No dependencies to install — uses only the Python standard library
```

## How to Run

### Play manually (human controls)
```bash
python main.py
```
Select **(m)anual** when prompted, then use **w/a/s/d** keys to move tiles.

### Let the AI play
```bash
python main.py
```
Select **(a)i** when prompted. The AI uses Expectimax search at depth 3.

### Compare all AI algorithms
```bash
python compare_algorithms.py
```
Runs Random, Greedy, Minimax, and Expectimax strategies on the same seed and prints a side-by-side comparison table.

---

## Code Ownership & Separation

> **The AI is a completely independent module. It shares zero code with the game engine. Every file inside `ai/` was written from scratch by Person 2 (and Person 3 for heuristic weights). No engine code was copied, modified, or re-used inside the AI.**

### What belongs to whom

| Owner | Directory / Files | What it contains |
|-------|-------------------|-----------------|
| **Person 1** (Engine) | `engine/state.py`, `engine/mechanics.py`, `engine/game.py`, `engine/__init__.py` | Game state representation, tile movement & merging, random tile spawning. **We did not write or modify any of these files.** |
| **Person 2** (AI) | `ai/expectimax.py`, `ai/search.py`, `ai/minimax.py`, `ai/greedy.py`, `ai/random_play.py`, `ai/__init__.py` | All search algorithms, decision-making logic, the public API used by `main.py`. **Written entirely by us from scratch.** |
| **Person 3** (Heuristics) | `ai/heuristics.py` | Board evaluation functions and tuned weights. **Written from scratch; no engine code reused.** |
| **Person 4** (Report & Benchmarks) | `compare_algorithms.py`, `report/` | Benchmark experiments, performance comparison across depths and heuristics, formal problem definition, report writing. |
| **Shared** | `main.py` | Entry point that imports from both `engine` and `ai` to connect them. |

### How the AI interacts with the engine

The AI **never** modifies engine internals. It only calls two things from the engine:

1. **`engine.mechanics.move(state, action)`** — applies a direction (up/down/left/right) and returns the resulting board **without** spawning a random tile. This lets the AI explore possible futures deterministically.
2. **`GameState` read-only methods** — `.get_actions()`, `.get_empty_cells()`, `.spawn_tile()`, `.is_terminal()`, `.board`, `.score`. These are the public interface provided by Person 1.

The AI never imports from `engine.game` (the random spawner). All randomness during search is handled by explicit enumeration of possible tile spawns inside our chance nodes.

```
┌─────────────────────────────────────────────────────┐
│  main.py  (game loop)                               │
│    ├── calls engine to create/update game state      │
│    └── calls ai.search.choose_best_action()          │
│              │                                       │
│              ▼                                       │
│  ┌──────────────────────────┐                        │
│  │  ai/  (our code)         │                        │
│  │  - expectimax.py         │──reads──▶ GameState    │
│  │  - minimax.py            │──calls──▶ move()       │
│  │  - greedy.py             │          (from engine)  │
│  │  - random_play.py        │                        │
│  │  - heuristics.py         │                        │
│  │  - search.py             │                        │
│  └──────────────────────────┘                        │
│              │                                       │
│       NO shared code                                 │
│       NO engine imports beyond the public API         │
│              │                                       │
│  ┌──────────────────────────┐                        │
│  │  engine/  (Person 1)     │                        │
│  │  - state.py              │                        │
│  │  - mechanics.py          │                        │
│  │  - game.py               │                        │
│  └──────────────────────────┘                        │
└─────────────────────────────────────────────────────┘
```

---

## Project Structure

```
2048-game/
├── engine/                   # Game Engine (Person 1) — NOT our code
│   ├── __init__.py
│   ├── state.py              # Immutable GameState (frozen dataclass, tuple board)
│   ├── mechanics.py          # Tile movement & merge logic (rotation-based)
│   └── game.py               # Random tile spawning (P(2)=0.9, P(4)=0.1)
│
├── ai/                       # AI Module — ALL our code (Person 2 + Person 3)
│   ├── __init__.py
│   ├── expectimax.py         # Depth-limited Expectimax search (max/chance nodes)
│   ├── search.py             # Public API — wraps search with timing & stats
│   ├── heuristics.py         # Board evaluation functions & tuned weights
│   ├── minimax.py            # Minimax search (adversarial comparison baseline)
│   ├── greedy.py             # Greedy depth-1 strategy
│   └── random_play.py        # Random move strategy
│
├── main.py                   # Entry point — manual or AI play
├── compare_algorithms.py     # Run all strategies & print comparison table
└── README.md                 # This file
```

---

## AI Algorithms

| Algorithm | Description | Typical Max Tile |
|-----------|-------------|-----------------|
| **Random** | Picks a uniformly random valid move | ~128 |
| **Greedy** | Picks the move with the best immediate heuristic score | ~512 |
| **Minimax (d=2)** | Adversarial search — assumes worst-case tile placement | ~512–1024 |
| **Expectimax (d=2)** | Probabilistic search — averages over all possible tile spawns | ~1024 |
| **Expectimax (d=3)** | Same as above with deeper lookahead | ~2048 |

### Why Expectimax over Minimax?

The random tile spawn in 2048 is **not adversarial** tiles appear uniformly at random, not in the worst possible position. Minimax treats nature as an opponent, making overly pessimistic decisions. Expectimax correctly models the probabilistic nature of tile spawning, leading to significantly better performance.

## Heuristics

The board evaluator (`ai/heuristics.py`) combines six weighted features:

| Heuristic | What it measures |
|-----------|-----------------|
| `empty_cells` | Number of empty cells (more = better) |
| `max_tile_value` | Value of the largest tile |
| `monotonicity` | Whether rows/columns are sorted |
| `smoothness` | Difference between adjacent tiles (lower = better) |
| `corner_bonus` | Bonus for keeping high tiles near corners |
| `merge_potential` | Count of adjacent equal tiles |

---

## Team

- **Person 1** — Game Engine (`engine/`)
- **Person 2** — AI Search Algorithms (`ai/expectimax.py`, `ai/search.py`, `ai/minimax.py`, `ai/greedy.py`, `ai/random_play.py`)
- **Person 3** — Heuristic Tuning (`ai/heuristics.py` weights)
- **Person 4** — Report & Benchmarks (`compare_algorithms.py`, experiments, formal problem definition, performance analysis)
