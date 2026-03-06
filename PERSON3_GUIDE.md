Person 3 — Heuristics & Evaluation Designer (Detailed Explanation)

- A heuristic function ℎ(𝑛) estimates the cost from a state 𝑛 to the goal.
- 2048 game has no goal, so we make a value function (V(s))=> goal: maximize value function

After one move, the "score" can for example be:
Score(LEFT)  = 1200
Score(RIGHT) = 300
Score(UP)    = 1100
Score(DOWN)  = 50

The value function consists therefore of these properties to consider:
- Empty Tiles: good with more empty tiles since more tiles => harder to move
- SortedTiles: Good players keep numbers ordered in one direction => combining equal numbers is easier
- Similarity: similarity measures how similar neighboring tiles are.
- CornerMaxTile: Good players keep the largest tile in a corner.
- Weighted Board Heuristic
- Measures how many merges are possible.

V(s) =
1000 * empty_tiles
+ 1.0 * monotonicity
- 0.1 * smoothness
+ 500 * corner
+ 1 * weighted_board
+ 10 * merges, where the numbers are weights. These must be tuned!!!

def evaluate(board):
    return (
        1000 * empty_tiles(board)
        + 1.0 * monotonicity(board)
        - 0.1 * smoothness(board)
        + 500 * corner(board)
        + weighted_board(board)
    )

## �� Person 3 — Heuristics & Evaluation Designer

This is CRITICAL for 2048 quality.

From Lecture 3:

> Heuristic function h(n) estimates cost to goal 

In 2048, goal isn't fixed — so you define a utility/evaluation function.

This person designs:

### Heuristics like:

* Number of empty tiles
* Monotonicity (values decreasing left→right)
* Smoothness (neighbor differences)
* Max tile in corner
* Weighted board evaluation
* Merge potential

### Tasks:

* Define evaluation function mathematically (for report!)
* Tune weights
* Benchmark different heuristics

This person is key for report Section 7 & 8 .