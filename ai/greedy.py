# ai/greedy.py
"""Greedy (depth-1) strategy — picks the move with the best immediate heuristic."""

from __future__ import annotations

import math
from typing import Callable, Optional, Tuple

from engine.state import GameState
from engine.mechanics import move as engine_move

EvalFn = Callable[[GameState], float]


def greedy_decision(
    state: GameState,
    evaluator: EvalFn,
) -> Tuple[Optional[str], float]:
    best_action: Optional[str] = None
    best_value = -math.inf

    for action in state.get_actions():
        moved_state, changed = engine_move(state, action)
        if not changed:
            continue
        val = evaluator(moved_state)
        if val > best_value:
            best_value = val
            best_action = action

    return best_action, best_value
