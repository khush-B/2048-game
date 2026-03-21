# ai/expectimax.py
"""
Depth-limited Expectimax search for 2048.

Tree structure
--------------
Max node  (player turn)  : picks the action with the highest expected value.
Chance node (random turn) : averages over every possible tile spawn weighted
                            by probability (0.9 for tile-2, 0.1 for tile-4,
                            uniform across empty cells).

Depth convention
----------------
`depth` counts full player-move plies.
  - max_node at depth 0 → evaluate immediately.
  - max_node at depth d → expand actions → chance_node at same d.
  - chance_node at d    → expand spawns  → max_node at d-1.

Performance helpers
-------------------
  - Transposition cache keyed on (board, depth, node_type).
  - Optional pruning of low-probability chance children when the board has
    many empty cells (star-1 / star-2 pruning idea).

This module is *pure search logic*; evaluation lives in heuristics.py.
"""

from __future__ import annotations

import math
from typing import Callable, Dict, Tuple

from engine.state import GameState
from engine.mechanics import move as engine_move  # move WITHOUT random spawn

# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------
EvalFn = Callable[[GameState], float]

# Cache key: (board_tuple, depth, node_type)
_CacheKey = Tuple[Tuple[Tuple[int, ...], ...], int, str]

# ---------------------------------------------------------------------------
# Statistics (mutable module-level counters — reset per decision)
# ---------------------------------------------------------------------------
_nodes_expanded: int = 0


def _reset_stats() -> None:
    global _nodes_expanded
    _nodes_expanded = 0


def get_nodes_expanded() -> int:
    return _nodes_expanded


# ---------------------------------------------------------------------------
# Max Node
# ---------------------------------------------------------------------------
def _max_node(
    state: GameState,
    depth: int,
    evaluator: EvalFn,
    cache: Dict[_CacheKey, float],
) -> float:
    """
    Player's turn — choose the best action.

    Returns the maximum expected value over all valid actions.
    """
    global _nodes_expanded

    # --- leaf check ---
    if depth == 0 or state.is_terminal():
        _nodes_expanded += 1
        return evaluator(state)

    # --- cache lookup ---
    key: _CacheKey = (state.board, depth, "max")
    if key in cache:
        return cache[key]

    _nodes_expanded += 1

    best = -math.inf
    for action in state.get_actions():
        # Apply movement ONLY (no random spawn)
        moved_state, changed = engine_move(state, action)
        if not changed:
            continue
        child_val = _chance_node(moved_state, depth, evaluator, cache)
        if child_val > best:
            best = child_val

    # If no valid action was found, treat as terminal
    if best == -math.inf:
        best = evaluator(state)

    cache[key] = best
    return best


# ---------------------------------------------------------------------------
# Chance Node
# ---------------------------------------------------------------------------

# Spawn probabilities
_PROB_2 = 0.9
_PROB_4 = 0.1

# When many cells are empty, evaluating every (cell × value) pair is
# expensive.  We can cap the number of cells considered.  Set to None
# to disable (exact search).
_MAX_CHANCE_CELLS: int | None = None  # None = no limit


def _chance_node(
    state: GameState,
    depth: int,
    evaluator: EvalFn,
    cache: Dict[_CacheKey, float],
) -> float:
    """
    Nature's turn — average over every possible random tile spawn.

    Each empty cell is equally likely.  In each cell a 2 appears with
    probability 0.9 and a 4 with probability 0.1.
    """
    global _nodes_expanded

    # --- leaf check ---
    if state.is_terminal():
        _nodes_expanded += 1
        return evaluator(state)

    # --- cache lookup ---
    key: _CacheKey = (state.board, depth, "chance")
    if key in cache:
        return cache[key]

    _nodes_expanded += 1

    empty_cells = state.get_empty_cells()
    n = len(empty_cells)

    if n == 0:
        # Board is full but still has merges — pass directly to max
        val = _max_node(state, depth - 1, evaluator, cache)
        cache[key] = val
        return val

    # Optional: limit cells for speed (star-2 style pruning)
    cells = empty_cells
    if _MAX_CHANCE_CELLS is not None and n > _MAX_CHANCE_CELLS:
        # Keep a sample — deterministic: first N cells (top-left bias is fine)
        cells = empty_cells[:_MAX_CHANCE_CELLS]
        n = len(cells)

    expected = 0.0
    cell_prob = 1.0 / n  # uniform distribution over empty cells

    for cell in cells:
        # Spawn a 2
        s2 = state.spawn_tile(cell, 2)
        val2 = _max_node(s2, depth - 1, evaluator, cache)

        # Spawn a 4
        s4 = state.spawn_tile(cell, 4)
        val4 = _max_node(s4, depth - 1, evaluator, cache)

        expected += cell_prob * (_PROB_2 * val2 + _PROB_4 * val4)

    cache[key] = expected
    return expected


# ---------------------------------------------------------------------------
# Public entry point (called by search.py)
# ---------------------------------------------------------------------------
def expectimax_decision(
    state: GameState,
    depth: int,
    evaluator: EvalFn,
) -> Tuple[str | None, float, int]:
    """
    Run expectimax from the root and return
      (best_action, best_value, nodes_expanded).

    `depth` is the number of full player-move plies to look ahead.
    """
    _reset_stats()
    cache: Dict[_CacheKey, float] = {}

    best_action: str | None = None
    best_value = -math.inf

    actions = state.get_actions()
    if not actions:
        return None, evaluator(state), get_nodes_expanded()

    for action in actions:
        moved_state, changed = engine_move(state, action)
        if not changed:
            continue
        value = _chance_node(moved_state, depth, evaluator, cache)
        if value > best_value:
            best_value = value
            best_action = action

    return best_action, best_value, get_nodes_expanded()
