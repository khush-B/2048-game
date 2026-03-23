# compare_algorithms.py
"""Run all four AI strategies and print a comparison table."""

from __future__ import annotations

import random
import time
from typing import Callable, Optional

from engine.state import GameState
from ai.heuristics import combined_evaluator
from ai.expectimax import expectimax_decision
from ai.minimax import minimax_decision
from ai.greedy import greedy_decision
from ai.random_play import random_decision


def _play_game(
    choose_fn: Callable[[GameState], Optional[str]],
    seed: int = 42,
    max_steps: int = 10_000,
) -> dict:
    rng = random.Random(seed)
    state = GameState.new(seed_tiles=2, rng=rng)
    steps = 0
    t0 = time.perf_counter()

    while steps < max_steps:
        if state.is_terminal():
            break
        action = choose_fn(state)
        if action is None:
            break
        if action not in state.get_actions():
            break
        state = state.apply_action(action, rng=rng)
        steps += 1

    elapsed = time.perf_counter() - t0
    max_tile = max(max(row) for row in state.board)
    return {
        "score": state.score,
        "max_tile": max_tile,
        "moves": steps,
        "time": round(elapsed, 2),
    }


def main():
    strategies = {
        "Random": lambda s: random_decision(s, rng=random.Random()),
        "Greedy": lambda s: greedy_decision(s, combined_evaluator)[0],
        "Minimax (d=2)": lambda s: minimax_decision(s, 2, combined_evaluator)[0],
        "Expectimax (d=2)": lambda s: expectimax_decision(s, 2, combined_evaluator)[0],
    }

    print(f"{'Strategy':<22} {'Score':>8} {'Max Tile':>10} {'Moves':>7} {'Time (s)':>10}")
    print("-" * 62)

    for name, choose_fn in strategies.items():
        print(f"Running {name}...", end=" ", flush=True)
        result = _play_game(choose_fn, seed=42)
        print("done.")
        print(f"{name:<22} {result['score']:>8} {result['max_tile']:>10} {result['moves']:>7} {result['time']:>10}")


if __name__ == "__main__":
    main()
