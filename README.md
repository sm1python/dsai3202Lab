## Question 1

### 1. Algorithm Used by the Explorer

The automated maze explorer uses the **right-hand rule algorithm**, a classic maze-solving technique. This rule involves the explorer always trying to turn **right** first, then **forward**, then **left**, and finally **backward** if no other option is available.

The core logic works like this:
- At each step, it attempts to **turn right** and move forward.
- If it can't move right, it tries moving **forward**, then **left**, and finally **turns around** if no other directions are available.
- This behavior is implemented in the `solve()` method, where the sequence of turning and checking directions ensures a consistent wall-following pattern.

### 2. Loop Detection Mechanism

To avoid getting stuck in **infinite loops**, the explorer uses a simple history-based check:
- It keeps track of the **last 3 moves** using a `deque` called `move_history`.
- If all three are the same (`(x, y)` repeated), it identifies this as being stuck in a loop.
- This is handled by the `is_stuck()` method.

When a loop is detected:
- The explorer attempts to **backtrack** to the last known position with multiple possible moves.

### 3. Backtracking Strategy

The backtracking strategy works as follows:
- When the explorer is stuck, it calls `backtrack()`, which either uses a previously stored backtrack path or generates one using `find_backtrack_path()`.
- The backtracking path is determined by scanning **past positions** (`self.moves`) in reverse, looking for a spot that had **more than one possible direction** (`count_available_choices()` > 1).
- The explorer then moves backward along this path to resume solving from a better location.
- During the maze run however, **no backtracking was necessary**, as shown by the stat:  
  > `Number of backtrack operations: 0`

### 4. Statistics Provided at the End

Upon completing the maze, the explorer prints a performance summary via `print_statistics()`. This includes:

| Metric                    | Value                   |
|---------------------------|-------------------------|
| **Total Time Taken**      | `42.34 seconds`         |
| **Total Moves Made**      | `1279`                  |
| **Backtrack Operations**  | `0`                     |
| **Average Moves/sec**     | `30.21`                 |

These statistics give insight into:
- The **efficiency** of the solver.
- Whether **looping or backtracking** occurred.
> **Note**: It took long because **visualization** wasn't disabled.

### Observation:

- The solver successfully navigated the maze **without visual backtracking**, implying the right-hand rule was sufficient.
- The move count (1279) is relatively high, which might suggest a **complex or winding maze**.

---
---

## Question 2

### Answered in `mian.py`

```python
# MPI setup
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
...
```
> Full code in main.py


### Output:
#### Maze Exploration Statistics

| Explorer | Total Time Taken | Total Moves Made | Backtrack Operations  | Average Moves/sec  |
|----------|------------------|------------------|-----------------------|--------------------|
| 1        | `0.00` seconds   | `1279`           | `0`                   | `1055383.60`       |
| 2        | `0.00` seconds   | `1279`           | `0`                   | `1050835.42`       |
| 3        | `0.00` seconds   | `1279`           | `0`                   | `781885.27`        |
| 4        | `0.00` seconds   | `1279`           | `0`                   | `1040037.77`       |

**Best Time:** `0.00` seconds with `1279` moves

---
---

## Question 3

### Setup Summary

To evaluate and compare the performance of multiple maze explorers, the following setup was used:

- **Maze Type:** Static Maze (same layout for all explorers)
- **Number of Explorers:** 4 (you can change it BTW)
- **Execution Method:** Parallel processing using **MPI4Py** (each process runs one or more explorers)
- **Visualization:** Disabled for performance accuracy
- **Metrics Collected:**
  - Total time taken
  - Number of moves
  - Number of backtrack operations (optional, not applicable here)

---

### Collected Results

All explorers solved the maze using the same logic and maze layout. Below are the aggregated results:

| Explorer | Time (s) | Moves | Backtracks |
|----------|----------|-------|------------|
| 1        | 0.00     | 1279  | 0          |
| 2        | 0.00     | 1279  | 0          |
| 3        | 0.00     | 1279  | 0          |
| 4        | 0.00     | 1279  | 0          |

---

### Analysis:

1. **Identical Results Across All Explorers**  
   All explorers completed the static maze using **exactly 1279 moves**, with **no backtracking** required. This consistency is expected because:
   - The maze structure and logic were identical.
   - The right-hand rule led them all down the same path.
   - There was no randomization in the starting or ending conditions or points.

2. **Extremely Fast Execution Times (0.00 seconds)**  
   The recorded execution time for each explorer was reported as `0.00 seconds`. This likely means:
   - The actual time was **less than 0.01 seconds**, rounding down in the float display.
   - The code executed almost instantly due to **disabled visualization** and **static maze predictability**.
   - The high performance metrics (`~1 million moves/sec`) confirm the speed.

3. **No Backtracking Needed**  
   Since the maze was straightforward for the right-hand rule algorithm, none of the explorers triggered the loop detection or backtracking logic.

4. **Parallel Execution Efficiency**  
   Running explorers in parallel using MPI ensured full CPU utilization across cores or machines. The performance gain here is in **reduced overall runtime** and **better scalability**, especially valuable when running many unique mazes or randomized inputs.

---
---

## Question 4

### 1. Identified Limitations

After analyzing the current implementation of the maze explorer (based on the **right-hand rule**), we identified the following key limitations:

- **Inefficient Navigation**  
  The right-hand rule often takes **unoptimal paths**, especially in open mazes. It blindly follows the right wall, which leads to unnecessary moves and longer solve times.

- **Poor Loop and Trap Detection**  
  Loop detection is minimal (only checks last 3 moves). It may not effectively prevent the explorer from revisiting the same areas in complex mazes (but that's not a problem for the right-wall rule but rather for all other techniques).

- **Limited Intelligence in Decision-Making**  
  The explorer doesn’t consider the actual **goal position** during navigation. It makes decisions based only on local surroundings, not the global structure of the maze.

---

### 2. Proposed Improvements

To overcome the above limitations, we propose the following enhancements:

| Improvement                          | Description                                                                 |
|--------------------------------------|-----------------------------------------------------------------------------|
| **A* Search Algorithm**              | Replace the wall-following logic with A*, a heuristic-based optimal path finder. |
| **Manhattan Distance Heuristic**     | Use a heuristic to estimate the cost from current cell to goal (faster search). |
| Smarter Loop Detection               | Implement history-based loop detection using a set of visited nodes.       |
| Dynamic Path Replanning              | Recompute the best path periodically if the maze or conditions change.     |

In this implementation, we have chosen to **implement the first two** improvements.

---

### 3. Implemented Enhancements

The following enhancements were added in `enhanced_explorer.py`:

#### A* Search Algorithm

We replaced the right-hand rule with the **A\*** algorithm. A* ensures the explorer finds the **shortest path** by using a priority queue (`heapq`) and tracking both actual path cost and estimated cost to goal:

```python
def a_star(self) -> List[Tuple[int, int]]:
    # Uses open_list (priority queue), came_from (parent links), and f/g scores
    # Manhattan distance is used as the heuristic
    ...
```

#### Manhattan Distance Heuristic

A simple but effective heuristic for grid-based pathfinding. It computes the distance in terms of grid steps:

```python
def heuristic(self, pos: Tuple[int, int], goal: Tuple[int, int]) -> int:
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
```

#### Updated Solve Logic

The `solve()` function now uses A* instead of manual movement and decisions. Once the optimal path is computed, the explorer simply follows it:

```python
def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
    path = self.a_star()
    self.move_to(path)
```

---

#### Modified Code Snippet

Here’s a brief excerpt from the updated explorer:

```python
def move_to(self, path: List[Tuple[int, int]]):
    for (target_x, target_y) in path:
        self.x, self.y = target_x, target_y
        self.moves.append((self.x, self.y))
        if self.visualize:
            self.draw_state()
```

This replaces complex wall-following logic with direct and efficient movement.

---

#### Benefits of Enhancements

- **Shorter Path Lengths** – Explorers using A* consistently choose optimal paths.
- **Faster Execution** – Fewer unnecessary moves means less time taken overall.
- **Goal-Aware Behavior** – Unlike the right-hand rule, A* actively seeks the end point using heuristics.

---

#### Summary

| Criteria                            | Original Explorer  | Enhanced Explorer (A*) |
|-------------------------------------|--------------------|------------------------|
| Algorithm Used                      | Right-hand rule    | A* Search              |
| Goal Awareness                      | No                 | Yes                    |
| Path Optimality                     | Suboptimal         | Optimal                |
| Loop/Trap Avoidance                 | Limited            | Avoids by design       |
| Performance in Static Maze          | Variable           | Consistent & fast      |

> **Conclusion**:  
> By replacing the local, rule-based strategy with A* search, we drastically improved both the **efficiency** and **intelligence** of the maze explorer.

---
---

## Question 5

### 1. Performance Results & Analysis

We compared both versions of the maze explorer — the **original** (right-hand rule) and the **enhanced** (A*) — on a static maze using 4 parallel runs each.

#### Collected Metrics

| Metric                      | Original Explorer         | Enhanced Explorer         |
|----------------------------|---------------------------|---------------------------|
| **Avg. Time Taken**        | 0.00 s                    | 0.00 s                    |
| **Avg. Moves Made**        | 1279                      | 127                       |
| **Backtrack Operations**   | 0                         | 0                         |
| **Avg. Moves/sec**         | ~988,880                  | ~70,363                   |


- **Original Explorer** wastes a large number of moves due to inefficient wall-following logic.  
- **Enhanced Explorer** uses A* to find the shortest path (127 moves), leading to dramatically fewer steps.

> **Note:** Time values are rounded to 0.00 seconds due to the speed of execution, but moves and efficiency clearly show performance differences.


---

### 2. Analysis of Results

#### Enhanced Explorer Advantages

| Advantage                          | Description                                                                 |
|------------------------------------|-----------------------------------------------------------------------------|
|    **Optimal Pathfinding**         | Consistently finds the shortest route (127 moves).                         |
|    **Zero Backtracking**           | A* avoids the need for backtracking by planning ahead.                     |
|    **Reduced Redundancy**          | Explorer avoids unnecessary loops or revisits.                             |
|    **Deterministic Output**        | Always finds the same shortest path.                                       |

#### Trade-offs & Limitations

| Trade-Off                          | Explanation                                                                 |
|------------------------------------|-----------------------------------------------------------------------------|
|    **Lower Raw Speed (Moves/sec)** | A* spends time planning, so actual move execution is slower.                |
|    **Requires Complete Maze Info** | A* needs the full maze structure before solving (not for fog-like mazes).   |

---

#### Final Verdict

| Category                | Winner          | Why?                                        |
|------------------------|-----------------|---------------------------------------------|
| **Total Moves**        | Enhanced        | Finds the shortest path                     |
| **CPU Efficiency**     | Original        | Raw move speed (less logic per step)        |
| **Smart Navigation**   | Enhanced        | Uses heuristics and avoids backtracking     |
| **Scalability**        | Enhanced        | Better suited for large/complex mazes       |

> 🏁 **Conclusion**:  
> The enhanced A* explorer **massively improves navigation quality** by reducing total moves from **1279 ➝ 127**. While the move-per-second rate is lower due to smarter planning, this is a worthy trade-off for much better efficiency and accuracy in pathfinding.

---
## Final point
| Explorer | Moves |
|----------|-------|
| # 1      | 127   |
> Does this mean i get 100% in both?

---

## Bonus points

1. Fastest solver to get top 10% routes (number of moves)
> hopefully i made it to here

2. Finding a solution with no backtrack operations
> A* doesnt need backtracking

3. Least number of moves.
> almost impossible but cant not hope

---
### Path taken by explorer (length 127):
```[(11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1), (17, 1), (18, 1), (19, 1), (20, 1), (21, 1), (22, 1), (23, 1), (23, 2), (23, 3), (24, 3), (25, 3), (26, 3), (27, 3), (28, 3), (29, 3), (29, 4), (29, 5), (30, 5), (31, 5), (32, 5), (33, 5), (34, 5), (35, 5), (36, 5), (37, 5), (38, 5), (38, 6), (38, 7), (37, 7), (36, 7), (35, 7), (35, 8), (35, 9), (35, 10), (35, 11), (35, 12), (35, 13), (35, 14), (35, 15), (36, 15), (37, 15), (38, 15), (39, 15), (40, 15), (41, 15), (41, 16), (41, 17), (41, 18), (41, 19), (40, 19), (39, 19), (38, 19), (38, 20), (38, 21), (38, 22), (38, 23), (38, 24), (38, 25), (37, 25), (36, 25), (35, 25), (35, 26), (35, 27), (35, 28), (35, 29), (35, 30), (34, 30), (33, 30), (32, 30), (32, 31), (32, 32), (32, 33), (32, 34), (32, 35), (32, 36), (31, 36), (30, 36), (29, 36), (29, 35), (29, 34), (28, 34), (27, 34), (26, 34), (25, 34), (24, 34), (23, 34), (23, 35), (23, 36), (24, 36), (25, 36), (26, 36), (26, 37), (26, 38), (27, 38), (28, 38), (29, 38), (29, 39), (29, 40), (28, 40), (27, 40), (26, 40), (25, 40), (24, 40), (23, 40), (23, 41), (23, 42), (23, 43), (23, 44), (23, 45), (23, 46), (22, 46), (21, 46), (20, 46), (19, 46), (18, 46), (17, 46), (16, 46), (15, 46), (14, 46), (13, 46), (13, 47)]
```



