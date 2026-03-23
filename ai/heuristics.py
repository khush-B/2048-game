# ai/heuristics.py
"""
Board evaluation functions for 2048 Expectimax.

Person 3 owns the final tuning and design of these heuristics.
This file ships with sensible defaults so the AI is playable immediately.

Every evaluator follows the signature:
    evaluator(state: GameState) -> float

Higher value = better board position.

Available heuristics
--------------------
  empty_cells      — counts empty tiles (more is better)
  max_tile_value   — value of the largest tile
  monotonicity     — reward rows/cols that are sorted
  smoothness       — penalise large differences between neighbours
  corner_bonus     — reward keeping the max tile in a corner
  merge_potential  — reward adjacent equal tiles
  combined_evaluator — weighted sum of all above (default)
"""

from __future__ import annotations

import math
from engine.state import GameState

SIZE = GameState.SIZE


# ---------------------------------------------------------------------------
# Individual heuristic components
# ---------------------------------------------------------------------------

def empty_cells(state: GameState) -> float:
    """More empty cells = more room to manoeuvre."""
    return float(len(state.get_empty_cells()))


def max_tile_value(state: GameState) -> float:
    """Log2 of the largest tile on the board."""
    m = max(max(row) for row in state.board)
    return math.log2(m) if m > 0 else 0.0


def monotonicity(state: GameState) -> float:
    """
    Reward boards where rows and columns are monotonically
    increasing or decreasing.  Compute penalty for violations
    in both directions and take the minimum penalty per line.
    """
    penalty = 0.0

    for r in range(SIZE):
        inc = 0.0
        dec = 0.0
        for c in range(SIZE - 1):
            cur = math.log2(state.board[r][c]) if state.board[r][c] else 0
            nxt = math.log2(state.board[r][c + 1]) if state.board[r][c + 1] else 0
            if cur > nxt:
                dec += nxt - cur  # negative
            else:
                inc += cur - nxt  # negative
        penalty += max(inc, dec)  # closer to 0 is better

    for c in range(SIZE):
        inc = 0.0
        dec = 0.0
        for r in range(SIZE - 1):
            cur = math.log2(state.board[r][c]) if state.board[r][c] else 0
            nxt = math.log2(state.board[r + 1][c]) if state.board[r + 1][c] else 0
            if cur > nxt:
                dec += nxt - cur
            else:
                inc += cur - nxt
        penalty += max(inc, dec)

    return penalty  # ≤ 0; higher (closer to 0) is better


def smoothness(state: GameState) -> float:
    """
    Penalise large value differences between adjacent tiles.
    Lower absolute difference = smoother = better.
    """
    penalty = 0.0
    for r in range(SIZE):
        for c in range(SIZE):
            v = math.log2(state.board[r][c]) if state.board[r][c] else 0
            if c + 1 < SIZE:
                nxt = math.log2(state.board[r][c + 1]) if state.board[r][c + 1] else 0
                penalty -= abs(v - nxt)
            if r + 1 < SIZE:
                nxt = math.log2(state.board[r + 1][c]) if state.board[r + 1][c] else 0
                penalty -= abs(v - nxt)
    return penalty  # ≤ 0


def corner_bonus(state: GameState) -> float:
    """
    Reward placing the max tile in a corner.
    Uses a snake-shaped weight matrix that strongly favours
    top-left corner strategy.
    """
    # Weight matrix — largest weights in top-right corner, decreasing in
    # a snake pattern.

    weights = (
        (4000, 6000, 8000, 10000),
        (1000, 800, 600, 400),
        (50, 100, 200, 300),
        (20, 15, 10, 0)
    )
  
    total = 0.0
    for r in range(SIZE):
        for c in range(SIZE):
            total += state.board[r][c] * weights[r][c]
    return total


def merge_potential(state: GameState) -> float:
    """Count pairs of adjacent equal non-zero tiles."""
    count = 0
    for r in range(SIZE):
        for c in range(SIZE):
            v = state.board[r][c]
            if v == 0:
                continue
            if c + 1 < SIZE and state.board[r][c + 1] == v:
                count += 1
            if r + 1 < SIZE and state.board[r + 1][c] == v:
                count += 1
    return float(count)


# ---------------------------------------------------------------------------
# Combined evaluator (default)
# ---------------------------------------------------------------------------

# Weights — Person 3 should tune these via experiments.
_W_EMPTY       =100 #100  #270.0 (empty: returns 0-16): more empty = good
_W_MAX_TILE    =100 #50  #0.0     (returns: 0-11, 0=tile2, 11=tile2048)
_W_MONOTONIC   = 0#200 #47.0 (returns: -40 to 0, where minus for messy boards)
_W_SMOOTH      = 0#200 #10.0 (returns: -69 to 0)
_W_CORNER      = 100 #1000 #Highest priority: highest tile in corner (1-16) => in start it is not important, but when high value tiles it is important!
_W_MERGE       = 0#40 #700.0 (returns: 0-8)
_W_SCORE       =0# 1000/10000 # this value increase fast! (returns: 0-50 000), 50 000 = goal???

def combined_evaluator(state: GameState) -> float:
    """
    Weighted combination of all heuristics.

    Returns a single float — higher is better.
    """
    return (
        _W_EMPTY     * empty_cells(state)
        + _W_MAX_TILE  * max_tile_value(state)
        + _W_MONOTONIC * monotonicity(state)
        + _W_SMOOTH    * smoothness(state)
        + _W_CORNER    * corner_bonus(state)
        + _W_MERGE     * merge_potential(state)
        + _W_SCORE     * state.score
    )

