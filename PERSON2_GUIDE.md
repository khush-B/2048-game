# Person 2 Guide: AI Search Developer (Expectimax)

## 1) Your Mission

You are responsible for the AI brain of the 2048 game.

Your job is to:
- Build Expectimax search.
- Make the AI choose the best move.
- Keep it fast enough to play smoothly.
- Work cleanly with the engine team using fixed interfaces.

At the end, your AI should play automatically and reach strong scores consistently.

---

## 2) What You Must Deliver

By project end, you should deliver:
- `ai/expectimax.py` (core search algorithm)
- `ai/search.py` (move selection wrapper)
- Optional helpers for performance (cache, move ordering)
- Simple logs for experiments (depth, nodes, score, time)
- Short technical note for report team (how your algorithm works)

---

## 3) Required Interface (Do Not Break This)

Your AI should only call engine methods like these:

- `state.get_actions()`
- `state.apply_action(action)`
- `state.get_empty_cells()`
- `state.spawn_tile(cell, value)`
- `state.is_terminal()`
- `state.clone()`
- `state.score`

If your engine names are slightly different, adapt only your AI wrapper, not engine logic.

---

## 4) Expectimax in Simple Words

In 2048 there are two kinds of turns:

1. **Player turn (Max node)**
   - AI chooses one move from: up, down, left, right.
   - Choose the move with highest expected value.

2. **Random turn (Chance node)**
   - After the move, game spawns a tile:
     - 2 with probability 0.9
     - 4 with probability 0.1
   - Tile appears in one empty cell.

So Expectimax means:
- Max node: take `max(...)`
- Chance node: take probability-weighted average

---

## 5) Step-by-Step Build Plan

### Step 1: Create the AI file structure

Create:
- `ai/expectimax.py`
- `ai/search.py`

In `search.py`, make one public function:
- `choose_best_action(state, depth, evaluator)`

This function will be called by `main.py`.

### Step 2: Build max node function

Create function:
- `expectimax_max(state, depth)`

Rules:
- If `depth == 0` or terminal: return evaluator score.
- Get valid actions.
- For each action:
  - Create next state with `apply_action`.
  - Call chance node.
- Return highest value.

### Step 3: Build chance node function

Create function:
- `expectimax_chance(state, depth)`

Rules:
- Get all empty cells.
- For each empty cell:
  - Add tile 2 (probability part = `0.9 / number_of_empty_cells`)
  - Add tile 4 (probability part = `0.1 / number_of_empty_cells`)
- Sum: `probability * child_value`
- Return expected value.

Important:
- After chance node, go back to max node with `depth - 1`.

### Step 4: Connect to evaluator

Do not hardcode heuristic inside search.

Pass evaluator function from Person 3:
- `evaluator(state) -> float`

This keeps clean separation.

### Step 5: Return the best action

In `choose_best_action(...)`:
- Loop through all valid actions.
- Compute expected value for each.
- Return action with highest value.

If no actions are valid, return `None`.

### Step 6: Add basic stats

Track:
- nodes expanded
- time per move
- selected action value

This helps Person 4 for benchmarks.

### Step 7: Add performance improvements

Add in this order:

1. **Move ordering**
   - Evaluate promising actions first (like actions that increase score or keep empty cells high).

2. **Transposition cache**
   - Key: board tuple + depth + node type
   - Value: computed expectimax value

3. **Adaptive depth (optional)**
   - If empty cells are many, use lower depth.
   - If board is crowded, use deeper search.

Keep code simple. Do not over-engineer.

---

## 6) Pseudocode (Reference)

```text
choose_best_action(state, depth, evaluator):
    best_action = None
    best_value = -infinity
    for action in state.get_actions():
        next_state = state.apply_action(action)
        value = expectimax_chance(next_state, depth - 1, evaluator)
        if value > best_value:
            best_value = value
            best_action = action
    return best_action

expectimax_max(state, depth, evaluator):
    if depth == 0 or state.is_terminal():
        return evaluator(state)
    value = -infinity
    for action in state.get_actions():
        child = state.apply_action(action)
        value = max(value, expectimax_chance(child, depth - 1, evaluator))
    return value

expectimax_chance(state, depth, evaluator):
    if depth == 0 or state.is_terminal():
        return evaluator(state)
    empty = state.get_empty_cells()
    if len(empty) == 0:
        return expectimax_max(state, depth, evaluator)
    expected = 0
    for cell in empty:
        s2 = state.spawn_tile(cell, 2)
        s4 = state.spawn_tile(cell, 4)
        expected += (0.9 / len(empty)) * expectimax_max(s2, depth, evaluator)
        expected += (0.1 / len(empty)) * expectimax_max(s4, depth, evaluator)
    return expected
```

---

## 7) Common Bugs (Avoid These)

- Reducing depth at both max and chance nodes incorrectly.
- Forgetting to divide spawn probability by number of empty cells.
- Mutating original state instead of using cloned/new state.
- Returning immediate score gain instead of expectimax value.
- Tight loops without cache causing very slow move selection.

---

## 8) Testing Checklist

Before handoff, verify:

- AI never picks invalid move.
- AI returns `None` only when game is terminal.
- With depth 2, move time is stable.
- With depth 3 or 4, AI quality improves.
- Same board state gives same selected action (deterministic search logic).
- Node count and move time are logged.

Quick test levels:
- Unit: one board, one move, expected best action.
- Integration: run full game with auto-play.
- Benchmark: run many games and collect mean score.

---

## 9) Week-by-Week Plan for Person 2

### Week 1 (Core Working Version)
- Implement max node and chance node.
- Connect to simple evaluator from Person 3.
- Auto-play works end-to-end.

### Week 2 (Quality and Speed)
- Add caching.
- Improve move ordering.
- Tune depth (2/3/4).

### Week 3 (Experiment Support)
- Freeze stable AI version.
- Generate benchmark logs for Person 4.
- Help explain algorithm section in report.

---

## 10) Handoff to Person 4 (Report Lead)

Provide this information clearly:
- Final algorithm: depth-limited expectimax
- Branching assumptions: up to 4 player moves, then chance over empty cells × 2 tile values
- Time cost per move by depth
- Average score and max tile by depth
- Number of nodes expanded per move

This directly supports report evaluation and grading.

---

## 11) Definition of Done

You are done when:
- AI plays complete games automatically.
- Code is separated cleanly from engine.
- AI uses expectimax correctly with probabilities.
- Performance is acceptable for repeated runs.
- Benchmark data is exportable for report.

If all above are true, Person 2 role is complete.
