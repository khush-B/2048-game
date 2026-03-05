# main.py
from __future__ import annotations

import random
from typing import Optional, Callable

from engine.state import GameState

# Optional: If you already have Person2's AI wrapper later, import it here.
# from ai.search import choose_best_action


KEYMAP = {
    "w": "up",
    "a": "left",
    "s": "down",
    "d": "right",
}

ACTION_TO_PRINT = {
    "up": "UP",
    "down": "DOWN",
    "left": "LEFT",
    "right": "RIGHT",
}


def format_board(state: GameState) -> str:
    """
    Produce exactly:
    Score: X

    a  b  c  d
    ...
    """
    lines = [f"Score: {state.score}", ""]
    for r in range(4):
        # two spaces between numbers, matching your example
        lines.append("  ".join(str(state.board[r][c]) for c in range(4)))
    return "\n".join(lines)


def max_tile(state: GameState) -> int:
    return max(max(row) for row in state.board)


def run_manual(state: GameState, rng: random.Random) -> GameState:
    print("Manual mode: use w/a/s/d. q to quit.\n")
    while True:
        print(format_board(state))
        print()

        if state.is_terminal():
            break

        key = input("Your move (w/a/s/d): ").strip().lower()
        if key == "q":
            return state
        if key not in KEYMAP:
            print("Invalid key.\n")
            continue

        action = KEYMAP[key]
        if action not in state.get_actions():
            print("Invalid move (board would not change).\n")
            continue

        state = state.apply_action(action, rng=rng)
        print()  # spacing

    return state


def default_ai_policy(state: GameState) -> Optional[str]:
    """
    Placeholder AI policy so main.py runs even before Person2 code exists.
    - picks the first valid action (not smart).
    Replace this with:
        choose_best_action(state, depth=3, evaluator=...)
    """
    actions = state.get_actions()
    return actions[0] if actions else None


def run_ai(
    state: GameState,
    rng: random.Random,
    choose_action_fn: Callable[[GameState], Optional[str]],
    max_steps: int = 10_000,
) -> GameState:
    print("AI mode.\n")
    steps = 0

    while steps < max_steps:
        print(format_board(state))
        print()

        if state.is_terminal():
            break

        action = choose_action_fn(state)
        if action is None:
            break

        # Print exactly like requested:
        print(f"AI chooses: {ACTION_TO_PRINT.get(action, action.upper())}")
        print()

        # Safety: if AI returns invalid move, stop to avoid infinite loop
        if action not in state.get_actions():
            print("AI returned invalid move. Stopping.\n")
            break

        state = state.apply_action(action, rng=rng)
        steps += 1

    return state


def main():
    rng = random.Random()  # set seed for reproducibility: random.Random(42)
    state = GameState.new(seed_tiles=2, rng=rng)

    mode = input("Choose mode: (m)anual or (a)i? ").strip().lower()
    print()

    if mode.startswith("a"):
        # Later swap default_ai_policy -> Person2 choose_best_action wrapper
        # e.g.:
        # evaluator = ...
        # choose_action = lambda s: choose_best_action(s, depth=3, evaluator=evaluator)
        choose_action = default_ai_policy
        state = run_ai(state, rng=rng, choose_action_fn=choose_action)
    else:
        state = run_manual(state, rng=rng)

    # End screen (exact 3 lines)
    if state.is_terminal():
        print("Game Over")
    else:
        # If user quit manual mode, still show summary (optional)
        print("Game Over")

    print(f"Final score: {state.score}")
    print(f"Max tile: {max_tile(state)}")


if __name__ == "__main__":
    main()