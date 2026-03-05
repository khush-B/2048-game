# Person 1 Guide: Game Engine Architect (2048 Engine)

## 1) Your Mission

You are responsible for the **game engine of 2048**.

Your job is to:

- Implement the full **2048 game mechanics**.
- Maintain the **game state**.
- Provide a **clean interface for the AI team**.
- Ensure the engine works **independently of the AI**.

The AI will only interact with the game through your engine.

By the end of **Week 1**, the engine must allow a **complete playable game**, even without AI.

------

# 2) What You Must Deliver

By project end, you should deliver:

- `engine/state.py` (game state representation)
- `engine/mechanics.py` (tile movement & merge logic)
- `engine/game.py` (game control functions)
- Core interface functions used by the AI
- Basic terminal board printing (text UI)

Your engine must be able to:

- start a new game
- apply moves
- spawn tiles
- detect terminal state

------

# 3) Required Interface (AI Depends on This)

Your engine must provide these methods:

```
state.get_actions()
state.apply_action(action)
state.get_empty_cells()
state.spawn_tile(cell, value)
state.is_terminal()
state.clone()
state.score
```

These functions are used by the AI search module.

Do **not change these names without informing Person 2**.

Person 2 will build Expectimax on top of them. PERSON2_GUIDE

------

# 4) Game State Representation

Create a `GameState` class.

Recommended representation:

```
4 × 4 matrix
```

Example board:

```
[2, 0, 0, 2]
[4, 2, 0, 0]
[0, 0, 4, 0]
[0, 0, 0, 0]
```

Where:

```
0 = empty cell
```

GameState should store:

```
board
score
```

Example structure:

```
class GameState:
    def __init__(self, board=None, score=0):
        self.board = board or [[0]*4 for _ in range(4)]
        self.score = score
```

------

# 5) Move Mechanics (Core Game Logic)

You must implement four moves:

```
UP
DOWN
LEFT
RIGHT
```

Each move performs:

### 1 Slide tiles

Example:

```
[2,0,2,0] → [2,2,0,0]
```

### 2 Merge equal tiles

Example:

```
[2,2,4,0] → [4,4,0,0]
```

### 3 Update score

If merge occurs:

```
2 + 2 → 4
score += 4
```

Important rule:

A tile can merge **only once per move**.

Example:

```
[2,2,2,2] → [4,4,0,0]
```

NOT

```
[8,0,0,0]
```

------

# 6) Implement get_actions()

Function:

```
state.get_actions()
```

Returns valid moves:

```
["up", "down", "left", "right"]
```

But **only if the move changes the board**.

Example:

If moving UP does nothing, do not include `"up"`.

------

# 7) Implement apply_action()

Function:

```
state.apply_action(action)
```

This should:

1. clone the state
2. apply movement
3. spawn random tile
4. return new state

Important:

**Do not modify the original state.**

AI search relies on immutable states.

------

# 8) Implement Random Tile Spawn

After each move:

Spawn tile in random empty cell.

Probability:

```
2 → 90%
4 → 10%
```

Example:

```
state.spawn_tile(cell, value)
```

Example empty cells:

```
[(0,1), (1,3), (2,2)]
```

Choose one randomly.

------

# 9) Implement get_empty_cells()

Return coordinates of empty cells.

Example output:

```
[(0,1), (1,3), (2,0)]
```

Used by AI for chance nodes.

------

# 10) Implement Terminal Test

Function:

```
state.is_terminal()
```

Game is terminal if:

```
no empty cells
AND
no valid moves
```

Check:

- horizontal merges
- vertical merges

------

# 11) Implement clone()

AI search needs to simulate future states.

```
state.clone()
```

Must return a **deep copy**.

Example:

```
def clone(self):
    return GameState(copy.deepcopy(self.board), self.score)
```

------

# 12) Basic Text UI (Optional but Helpful)

Add simple board printing.

Example output:

```
Score: 120

2 0 0 2
4 4 2 0
0 8 0 0
0 0 0 0
```

Simple keyboard controls for manual play:

```
w → up
s → down
a → left
d → right
```

This helps debug engine before AI integration.

------

# 13) Testing Checklist

Before handing engine to Person 2, verify:

- Moves follow official 2048 rules
- Score updates correctly
- Random tiles spawn correctly
- Invalid moves are rejected
- Game ends correctly
- `clone()` works properly
- `apply_action()` does not mutate original state

Manual testing example:

```
start game
make 50 moves
check score
check merges
```

------

# 14) Week-by-Week Plan for Person 1

### Week 1 (Core Engine)

Implement:

- board representation
- move logic
- merging rules
- random tile spawn
- terminal detection

Goal:

Playable 2048 in terminal.

------

### Week 2 (Integration)

Support AI:

- clone()
- get_actions()
- apply_action()
- empty cell detection

Fix bugs found during AI testing.

------

### Week 3 (Stability)

Finalize engine.

Tasks:

- optimize move code
- clean interface
- ensure deterministic behavior for testing
- help report team explain game rules.

------

# 15) Handoff to Person 2

Before AI development starts, confirm:

Engine provides:

```
state.get_actions()
state.apply_action(action)
state.get_empty_cells()
state.spawn_tile(cell,value)
state.is_terminal()
state.clone()
state.score
```

Person 2’s Expectimax will use these functions directly. PERSON2_GUIDE

------

# 16) Definition of Done

You are done when:

- The engine runs a complete 2048 game.
- All moves follow official rules.
- State transitions are correct.
- AI can interact using the provided interface.
- Code is cleanly separated from AI.

If all these are satisfied, the **Person 1 role is complete**.