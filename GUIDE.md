ChatGPT recommendation on how to divide the task for 4 people: 

Great choice with **2048** �� It’s actually a very good fit for 02180 because it’s:

* Single-player
* Stochastic (random tile spawns)
* Perfect information
* Very large state space
* Naturally solved with search (expectimax / best-first variants)

And since the assignment is weighted **50% implementation, 50% report** , you should divide work both technically and academically — not just coding.

Below is a **clean, 3-week, 4-person division plan** so you can work independently and efficiently.

---

# �� High-Level Architecture (VERY Important)

Before dividing work:

�� **Separate Game Engine and AI completely.**

The assignment explicitly requires that AI and engine are clearly separated .

So structure like this:

```
/engine
    game.py
    state.py
    mechanics.py

/ai
    search.py
    heuristics.py
    expectimax.py

/main.py
/report
```

That way people can work independently.

---

# �� Clean Task Division for 4 People

## �� Person 1 — Game Engine Architect

### Responsible for:

* Implementing 2048 rules
* State representation
* Move generation
* Random tile spawn
* Terminal test

### Specifically:

* `State` class (board as 4x4 matrix)
* `Actions(s)` → {up, down, left, right}
* `Result(s, a)`
* `Terminal-Test(s)`
* Score handling

### Deliverable:

Fully playable text-based 2048.

This person must finish Week 1.

---

## �� Person 2 — AI Search Developer

This is the “core AI person”.

Since 2048 is stochastic, you should use:

> ✅ **Expectimax** (not minimax)

Because:

* Player move = max node
* Random tile spawn = chance node (0.9 for 2, 0.1 for 4)

This fits perfectly with search from Lecture 2–3  .

### Responsible for:

* Search tree implementation
* Depth-limited expectimax
* Proper node expansion
* Performance optimisation

### Deliverable:

AI that can play automatically (even if bad initially).

---

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

---

## �� Person 4 — Report & Benchmark Lead

Very important role.

This person:

### Responsible for:

* Writing formal problem definition:

  * s₀
  * Actions(s)
  * Result(s,a)
  * Utility(s,p)
* State space size estimation
* Explaining stochastic nature
* Explaining why expectimax fits
* Benchmark experiments
* Comparing depths
* Comparing heuristics
* Measuring performance

This role is NOT passive. It is heavy.

They should also:

* Run 100 games per configuration
* Make plots
* Compare:

  * Depth 2 vs 3 vs 4
  * Different evaluation functions
  * Nodes expanded

This is directly required in the report .

---

# �� 3-Week Timeline

## Week 1 — Foundation

* Person 1: Finish engine
* Person 2: Skeleton expectimax
* Person 3: Draft heuristics
* Person 4: Start report structure + formal problem modeling

Goal: AI can run, even if weak.

---

## Week 2 — Intelligence

* Improve expectimax
* Add pruning optimisations
* Tune heuristic weights
* Benchmark different depths
* Start writing results section

Goal: AI reaches 2048 consistently.

---

## Week 3 — Polish & Benchmark

* Run experiments
* Compare versions
* Clean code separation
* Write final report
* Optimise performance
* Create readme

---

# ⚡ How To Work Independently

To avoid blocking each other:

### Define clear interfaces early:

```python
class GameState:
    def get_actions(self)
    def apply_action(self, action)
    def is_terminal(self)
    def clone(self)
```

AI only interacts with this interface.

Engine people never touch AI code.
AI people never touch engine logic.

---

# �� What Makes a High Grade Project

From assessment criteria :

They evaluate:

* Choice of algorithm
* Data structures
* Mathematical precision
* Quality of evaluation function
* Benchmarks
* Clear separation AI/engine

So what impresses them?

✅ Proper expectimax
✅ Clean state representation
✅ Smart heuristic explanation
✅ Performance comparison
✅ Mathematical clarity

---

# �� Bonus (If You Want A 12)

You can compare:

* Greedy search vs Expectimax
* Depth-limited vs iterative deepening
* Different heuristic combinations

Or show how heuristic dominance works (Lecture 3 idea) .

---

# �� Most Important Advice

Don’t make it too complex.

Depth 3–4 expectimax with strong heuristic is enough.

Do NOT try neural networks.

---

# �� Final Recommended Division

| Person | Role                 | Workload |
| ------ | -------------------- | -------- |
| 1      | Game engine          | Medium   |
| 2      | Search algorithm     | High     |
| 3      | Heuristic design     | High     |
| 4      | Report + experiments | High     |

Search + heuristics + benchmarking are where most grades come from.

---

If you want, I can next:

* Help you define the formal problem formulation for 2048 (s₀, Actions, etc.)
* Help you design a strong heuristic
* Help you sketch the expectimax structure
* Help you estimate the state space size properly for the report

What do you want to tackle first?
