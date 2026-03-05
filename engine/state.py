from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple
import copy

Cell = Tuple[int, int]  # (row, col)


@dataclass(frozen=True)
class GameState:
    """
    Immutable-ish state container for 2048.
    - board: 4x4 grid, 0 means empty
    - score: accumulated merge score
    """
    board: Tuple[Tuple[int, ...], ...]
    score: int = 0

    SIZE: int = 4

    @staticmethod
    def new(seed_tiles: int = 2, rng=None) -> "GameState":
        """Create a fresh game state and spawn initial tiles."""
        from .game import spawn_random_tile  # local import to avoid cycles

        empty_board = tuple(tuple(0 for _ in range(GameState.SIZE)) for _ in range(GameState.SIZE))
        s = GameState(board=empty_board, score=0)

        # Spawn initial tiles
        for _ in range(seed_tiles):
            s = spawn_random_tile(s, rng=rng)

        return s

    # ---------- Required Interface ----------

    def clone(self) -> "GameState":
        """Return a deep copy (GameState is tuple-based, but keep interface)."""
        return GameState(board=copy.deepcopy(self.board), score=self.score)

    def get_empty_cells(self) -> List[Cell]:
        empty: List[Cell] = []
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if self.board[r][c] == 0:
                    empty.append((r, c))
        return empty

    def spawn_tile(self, cell: Cell, value: int) -> "GameState":
        """
        Place a tile (2 or 4) at given empty cell.
        Must NOT mutate current state. Return a new state.
        """
        r, c = cell
        if self.board[r][c] != 0:
            raise ValueError(f"Cell {cell} is not empty; cannot spawn tile.")

        new_board = [list(row) for row in self.board]
        new_board[r][c] = value
        return GameState(board=tuple(tuple(row) for row in new_board), score=self.score)

    def is_terminal(self) -> bool:
        """
        Terminal when:
        - no empty cells AND
        - no valid moves (no merges possible)
        """
        if self.get_empty_cells():
            return False

        # Check if any adjacent equal tiles exist (horizontal/vertical)
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                v = self.board[r][c]
                if r + 1 < self.SIZE and self.board[r + 1][c] == v:
                    return False
                if c + 1 < self.SIZE and self.board[r][c + 1] == v:
                    return False

        return True

    def get_actions(self) -> List[str]:
        """
        Return valid actions among: ["up","down","left","right"]
        Only include moves that change the board.
        """
        from .mechanics import move  # local import to avoid cycles

        actions = []
        for a in ("up", "down", "left", "right"):
            moved_state, changed = move(self, a)
            if changed:
                actions.append(a)
        return actions

    def apply_action(self, action: str, rng=None) -> "GameState":
        """
        Apply a player move:
        - do the move/merge
        - if changed, spawn a random tile (2 with 0.9, 4 with 0.1)
        - return new state
        If move is invalid (no change), return the same state (or raise).
        """
        from .mechanics import move
        from .game import spawn_random_tile

        moved_state, changed = move(self, action)
        if not changed:
            # For AI safety: returning self keeps it pure; AI should not pick invalid moves anyway.
            return self

        return spawn_random_tile(moved_state, rng=rng)

    # ---------- Helpers ----------

    def to_pretty_string(self) -> str:
        lines = [f"Score: {self.score}"]
        for r in range(self.SIZE):
            lines.append(" ".join(f"{self.board[r][c]:4d}" for c in range(self.SIZE)))
        return "\n".join(lines)