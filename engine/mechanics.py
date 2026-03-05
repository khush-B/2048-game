from __future__ import annotations

from typing import List, Tuple
from .state import GameState


def _compress(row: List[int]) -> List[int]:
    """Slide non-zero tiles to the left."""
    return [x for x in row if x != 0]


def _merge_left(row: List[int]) -> Tuple[List[int], int]:
    """
    Merge a single row assuming it is already compressed to the left.
    Rule: each tile can merge at most once per move.
    Returns: (new_row, gained_score)
    """
    gained = 0
    new_row: List[int] = []
    skip = False

    for i in range(len(row)):
        if skip:
            skip = False
            continue

        if i + 1 < len(row) and row[i] == row[i + 1]:
            merged = row[i] * 2
            new_row.append(merged)
            gained += merged
            skip = True
        else:
            new_row.append(row[i])

    # pad with zeros to length 4
    while len(new_row) < GameState.SIZE:
        new_row.append(0)

    return new_row, gained


def _move_left_board(board: Tuple[Tuple[int, ...], ...]) -> Tuple[Tuple[Tuple[int, ...], ...], int]:
    """
    Apply left move on board only.
    Returns (new_board, gained_score).
    """
    gained_total = 0
    new_rows: List[Tuple[int, ...]] = []

    for r in range(GameState.SIZE):
        row = list(board[r])
        compressed = _compress(row)
        merged_row, gained = _merge_left(compressed)
        gained_total += gained
        new_rows.append(tuple(merged_row))

    return tuple(new_rows), gained_total


def _rotate_board_cw(board: Tuple[Tuple[int, ...], ...]) -> Tuple[Tuple[int, ...], ...]:
    """Rotate board clockwise."""
    size = GameState.SIZE
    return tuple(
        tuple(board[size - 1 - r][c] for r in range(size))
        for c in range(size)
    )


def _rotate_board_ccw(board: Tuple[Tuple[int, ...], ...]) -> Tuple[Tuple[int, ...], ...]:
    """Rotate board counter-clockwise."""
    size = GameState.SIZE
    return tuple(
        tuple(board[r][size - 1 - c] for r in range(size))
        for c in range(size)
    )


def _rotate_board_180(board: Tuple[Tuple[int, ...], ...]) -> Tuple[Tuple[int, ...], ...]:
    """Rotate board 180 degrees."""
    size = GameState.SIZE
    return tuple(
        tuple(board[size - 1 - r][size - 1 - c] for c in range(size))
        for r in range(size)
    )


def move(state: GameState, action: str) -> Tuple[GameState, bool]:
    """
    Apply movement/merge ONLY (no random spawn here).
    Returns (new_state, changed)
    """
    action = action.lower().strip()
    b = state.board
    gained = 0

    if action == "left":
        new_b, gained = _move_left_board(b)

    elif action == "right":
        b180 = _rotate_board_180(b)
        moved, gained = _move_left_board(b180)
        new_b = _rotate_board_180(moved)

    elif action == "up":
        ccw = _rotate_board_ccw(b)
        moved, gained = _move_left_board(ccw)
        new_b = _rotate_board_cw(moved)

    elif action == "down":
        cw = _rotate_board_cw(b)
        moved, gained = _move_left_board(cw)
        new_b = _rotate_board_ccw(moved)

    else:
        raise ValueError(f"Unknown action: {action}. Use up/down/left/right.")

    changed = (new_b != b)
    new_state = GameState(board=new_b, score=state.score + gained)
    return new_state, changed