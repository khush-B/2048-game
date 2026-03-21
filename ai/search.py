# ai/search.py
"""
Public AI interface — the only module that main.py needs to import.

Usage
-----
    from ai.search import choose_best_action
    from ai.heuristics import combined_evaluator

    action = choose_best_action(state, depth=3, evaluator=combined_evaluator)

The function returns the best action string ("up", "down", "left", "right")
or None when the game is over.

It also prints lightweight per-move stats (nodes, time) to stdout so that
Person 4 can capture benchmark data.
"""

from __future__ import annotations

import time
from typing import Callable, Optional

from engine.state import GameState
from ai.expectimax import expectimax_decision

# Type alias for evaluator functions
EvalFn = Callable[[GameState], float]


# ---------------------------------------------------------------------------
# Cumulative session stats (optional — useful for benchmarks)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Main public function
# ---------------------------------------------------------------------------
def choose_best_action(
    state: GameState,
    depth: int = 3,
    evaluator: EvalFn | None = None,
    verbose: bool = False,
) -> Optional[str]:
    """
    Choose the best action for the given state using Expectimax search.

    Parameters
    ----------
    state : GameState
        Current board state from the engine.
    depth : int
        Number of full player-move plies to look ahead. (2-4 recommended)
    evaluator : callable(GameState) -> float
        Board evaluation / heuristic function (from Person 3).
        If None, falls back to a basic built-in evaluator.
    verbose : bool
        If True, print per-move stats to stdout.

    Returns
    -------
    str or None
        Best action ("up"/"down"/"left"/"right") or None if terminal.
    """
    global _total_nodes, _total_moves, _total_time

    # Fallback evaluator if Person 3 hasn't delivered yet
    if evaluator is None:
        from ai.heuristics import combined_evaluator
        evaluator = combined_evaluator

    t0 = time.perf_counter()
    best_action, best_value, nodes = expectimax_decision(state, depth, evaluator)
    elapsed = time.perf_counter() - t0

    # Update session stats
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
