# ai/minimax.py
"""Minimax search (adversarial) for 2048 — comparison baseline."""

from __future__ import annotations

import math
from typing import Callable, Dict, Optional, Tuple

from engine.state import GameState
from engine.mechanics import move as engine_move

EvalFn = Callable[[GameState], float]
_CacheKey = Tuple[Tuple[Tuple[int, ...], ...], int, str]

_nodes_expanded: int = 0


def _reset_stats() -> None:
    global _nodes_expanded
    _nodes_expanded = 0


def _max_node(
    state: GameState,
    depth: int,
    evaluator: EvalFn,
    cache: Dict[_CacheKey, float],
) -> float:
    global _nodes_expanded

    if depth == 0 or state.is_terminal():
        _nodes_expanded += 1
        return evaluator(state)

    key: _CacheKey = (state.board, depth, "max")
    if key in cache:
        return cache[key]

    best = -math.inf
    for action in state.get_actions():
        moved_state, changed = engine_move(state, action)
        if not changed:
            continue
        val = _min_node(moved_state, depth, evaluator, cache)
        if val > best:
            best = val
        _nodes_expanded += 1

    if best == -math.inf:
        best = evaluator(state)

    cache[key] = best
    return best


def _min_node(
    state: GameState,
    depth: int,
    evaluator: EvalFn,
    cache: Dict[_CacheKey, float],
) -> float:
    """Adversary places worst-case tile in an empty cell."""
    global _nodes_expanded

    if state.is_terminal():
        _nodes_expanded += 1
        return evaluator(state)

    key: _CacheKey = (state.board, depth, "min")
    if key in cache:
        return cache[key]

    empty_cells = state.get_empty_cells()
    if not empty_cells:
        val = _max_node(state, depth - 1, evaluator, cache)
        cache[key] = val
        return val

    worst = math.inf
    for cell in empty_cells:
        for value in (2, 4):
            child = state.spawn_tile(cell, value)
            val = _max_node(child, depth - 1, evaluator, cache)
            if val < worst:
                worst = val
            _nodes_expanded += 1

    cache[key] = worst
    return worst


def minimax_decision(
    state: GameState,
    depth: int,
    evaluator: EvalFn,
) -> Tuple[Optional[str], float, int]:
    global _nodes_expanded
    _reset_stats()
    cache: Dict[_CacheKey, float] = {}

    best_action: Optional[str] = None
    best_value = -math.inf

    for action in state.get_actions():
        moved_state, changed = engine_move(state, action)
        if not changed:
            continue
        val = _min_node(moved_state, depth, evaluator, cache)
        _nodes_expanded += 1
        if val > best_value:
            best_value = val
            best_action = action

    return best_action, best_value, _nodes_expanded
