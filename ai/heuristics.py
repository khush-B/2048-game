# ai/heuristics.py
"""Board evaluation functions for 2048 Expectimax."""

from __future__ import annotations

import math
from engine.state import GameState

SIZE = GameState.SIZE


def empty_cells(state: GameState) -> float:
    return float(len(state.get_empty_cells()))


def max_tile_value(state: GameState) -> float:
    m = max(max(row) for row in state.board)
    return math.log2(m) if m > 0 else 0.0


def monotonicity(state: GameState) -> float:
    penalty = 0.0

    for r in range(SIZE):
        inc = 0.0
        dec = 0.0
        for c in range(SIZE - 1):
            cur = math.log2(state.board[r][c]) if state.board[r][c] else 0
            nxt = math.log2(state.board[r][c + 1]) if state.board[r][c + 1] else 0
            if cur > nxt:
                dec += nxt - cur
            else:
                inc += cur - nxt
        penalty += max(inc, dec)

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

    return penalty


def smoothness(state: GameState) -> float:
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
    return penalty


def corner_bonus(state: GameState) -> float:
    weights = (
        (4000, 6000, 8000, 10000),
        (1000, 800, 600, 400),
        (50, 100, 200, 300),
        (20, 15, 10, 0),
    )
    total = 0.0
    for r in range(SIZE):
        for c in range(SIZE):
            total += state.board[r][c] * weights[r][c]
    return total


def merge_potential(state: GameState) -> float:
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


_W_EMPTY     = 100
_W_MAX_TILE  = 100
_W_MONOTONIC = 0
_W_SMOOTH    = 0
_W_CORNER    = 100
_W_MERGE     = 0
_W_SCORE     = 0


def combined_evaluator(state: GameState) -> float:
    return (
        _W_EMPTY     * empty_cells(state)
        + _W_MAX_TILE  * max_tile_value(state)
        + _W_MONOTONIC * monotonicity(state)
        + _W_SMOOTH    * smoothness(state)
        + _W_CORNER    * corner_bonus(state)
        + _W_MERGE     * merge_potential(state)
        + _W_SCORE     * state.score
    )

