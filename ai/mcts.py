# ai/mcts.py
"""Monte Carlo Tree Search (MCTS) for 2048."""

from __future__ import annotations

import math
import random
from typing import Optional

from engine.state import GameState
from engine.mechanics import move as engine_move


class _MCTSNode:
    __slots__ = ("state", "action", "parent", "children",
                 "visits", "total_reward", "untried_actions")

    def __init__(self, state: GameState, action: Optional[str] = None,
                 parent: Optional["_MCTSNode"] = None):
        self.state = state
        self.action = action
        self.parent = parent
        self.children: list[_MCTSNode] = []
        self.visits = 0
        self.total_reward = 0.0
        self.untried_actions = list(state.get_actions())

    def is_fully_expanded(self) -> bool:
        return len(self.untried_actions) == 0

    def best_child(self, c: float = 1.41) -> "_MCTSNode":
        best = None
        best_ucb = -math.inf
        for child in self.children:
            exploit = child.total_reward / child.visits
            explore = c * math.sqrt(math.log(self.visits) / child.visits)
            ucb = exploit + explore
            if ucb > best_ucb:
                best_ucb = ucb
                best = child
        return best


def _random_rollout(state: GameState, rng: random.Random, max_depth: int = 40) -> float:
    for _ in range(max_depth):
        if state.is_terminal():
            break
        actions = state.get_actions()
        if not actions:
            break
        action = rng.choice(actions)
        state = state.apply_action(action, rng=rng)
    return float(state.score)


def _tree_policy(node: _MCTSNode, rng: random.Random) -> _MCTSNode:
    while not node.state.is_terminal():
        if not node.is_fully_expanded():
            return _expand(node, rng)
        node = node.best_child()
    return node


def _expand(node: _MCTSNode, rng: random.Random) -> _MCTSNode:
    action = node.untried_actions.pop()
    moved_state, changed = engine_move(node.state, action)
    if changed:
        child_state = moved_state.apply_action(action, rng=rng)
        child_state = GameState(board=moved_state.board, score=moved_state.score)
        empty = moved_state.get_empty_cells()
        if empty:
            cell = rng.choice(empty)
            value = 2 if rng.random() < 0.9 else 4
            child_state = moved_state.spawn_tile(cell, value)
        else:
            child_state = moved_state
    else:
        child_state = node.state

    child = _MCTSNode(child_state, action=action, parent=node)
    node.children.append(child)
    return child


def _backpropagate(node: _MCTSNode, reward: float) -> None:
    while node is not None:
        node.visits += 1
        node.total_reward += reward
        node = node.parent


def mcts_decision(
    state: GameState,
    iterations: int = 500,
    rng: random.Random | None = None,
) -> Optional[str]:
    if state.is_terminal():
        return None

    rng = rng or random.Random()
    root = _MCTSNode(state)

    for _ in range(iterations):
        leaf = _tree_policy(root, rng)
        reward = _random_rollout(leaf.state, rng)
        _backpropagate(leaf, reward)

    if not root.children:
        actions = state.get_actions()
        return actions[0] if actions else None

    best = max(root.children, key=lambda c: c.visits)
    return best.action
