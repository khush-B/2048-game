# ai/random_play.py
"""Random strategy — picks a uniformly random valid move."""

from __future__ import annotations

import random
from typing import Optional

from engine.state import GameState


def random_decision(
    state: GameState,
    rng: random.Random | None = None,
) -> Optional[str]:
    actions = state.get_actions()
    if not actions:
        return None
    r = rng or random
    return r.choice(actions)
