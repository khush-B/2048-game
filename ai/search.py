# ai/search.py
"""Public AI interface for main.py."""

from __future__ import annotations

import time
from typing import Callable, Optional

from engine.state import GameState
from ai.expectimax import expectimax_decision

EvalFn = Callable[[GameState], float]


_total_nodes: int = 0
_total_moves: int = 0
_total_time: float = 0.0


def reset_session_stats() -> None:
    global _total_nodes, _total_moves, _total_time
    _total_nodes = 0
    _total_moves = 0
    _total_time = 0.0


def get_session_stats() -> dict:
    return {
        "total_moves": _total_moves,
        "total_nodes": _total_nodes,
        "total_time_s": round(_total_time, 4),
        "avg_nodes_per_move": round(_total_nodes / max(_total_moves, 1), 1),
        "avg_time_per_move_s": round(_total_time / max(_total_moves, 1), 4),
    }


def choose_best_action(
    state: GameState,
    depth: int = 3,
    evaluator: EvalFn | None = None,
    verbose: bool = False,
) -> Optional[str]:
    global _total_nodes, _total_moves, _total_time

    if evaluator is None:
        from ai.heuristics import combined_evaluator
        evaluator = combined_evaluator

    t0 = time.perf_counter()
    best_action, best_value, nodes = expectimax_decision(state, depth, evaluator)
    elapsed = time.perf_counter() - t0

    _total_nodes += nodes
    _total_moves += 1
    _total_time += elapsed

    if verbose:
        print(
            f"  [AI] depth={depth}  action={best_action}  "
            f"value={best_value:,.1f}  nodes={nodes:,}  "
            f"time={elapsed:.3f}s"
        )

    return best_action
