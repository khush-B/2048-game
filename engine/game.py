from __future__ import annotations

from typing import Optional
import random
from .state import GameState


def spawn_random_tile(state: GameState, rng: Optional[random.Random] = None) -> GameState:
    """
    Spawn a random tile into a random empty cell:
    - value 2 with prob 0.9
    - value 4 with prob 0.1
    Return new state (do not mutate).
    """
    rng = rng or random
    empty = state.get_empty_cells()
    if not empty:
        return state  # no place to spawn; happens at terminal or full board

    cell = rng.choice(empty)
    value = 2 if rng.random() < 0.9 else 4
    return state.spawn_tile(cell, value)