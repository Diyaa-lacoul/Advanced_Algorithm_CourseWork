# Advanced_Algorithm_CourseWork
# ST5003CEM Advanced Algorithms - Quick Reference Guide
**Module:** Advanced Algorithms  
**Assignment:** Coursework (Due: 25 Jan 2026)  
**Format:** Quick Reference with Code Examples

---

## 📋 Problem Overview

| # | Problem | File | Method | I/O |
|---|---------|------|--------|-----|
| 1a | Sensor Placement | `Task1a.py` | Weiszfeld Iteration | Coordinates → Distance |
| 1b | Traveling Salesman | `Task1b.py` | Simulated Annealing | Cities → Tour Cost |
| 2 | Tile Shatter Game | `Task2.py` | Dynamic Programming | Multipliers → Max Points |
| 3 | Min Service Centers | `Task3.py` | Tree DFS Greedy | TreeNode → Center Count |
| 4 | Energy Grid | `Task4.py` | Greedy Allocation | Demand → Allocation Plan |
| 5a | Network Simulator | `Task5a.py` | Graph Algorithms | Network Graph → MST/Paths |
| 5b | Multithreaded Sort | `Task5b.py` | QuickSort + Threads | Array → Sorted Array |
| 6 | Robot Delivery | `Task6.py` | DFS/BFS/A* Search | Graph → Optimal Path |

---



### 1A: Optimal Sensor Placement
```
Input:  [[0,1], [1,0], [1,2], [2,1]]
Output: 4.0
Method: Weiszfeld Algorithm
Complexity: O(I × N) where I ≈ 100 iterations
```

**Key Function:**
```python
find_optimal_hub(sensor_locations) → float
```

**How It Works:**
1. Start at centroid (mean of all points)
2. Iteratively move toward geometric median
3. Weight by inverse distance: w = 1/d
4. Stop when movement < 1e-7

---

### 1B: Traveling Salesman Problem
```
Input:  30 random cities in [0,100]²
Output: Tour distance (minimized)
Method: Simulated Annealing with 2-opt
```

**Key Classes:**
```python
class ExponentialSchedule: temperature_at_iteration(k) → float
class LinearSchedule: temperature_at_iteration(k) → float
class TSPSimulatedAnnealingSolver: solve(schedule) → (tour, distance)
```

**Cooling Schedules:**
- **Exponential:** T_k = T₀ × 0.9995^k (slower cooling)
- **Linear:** T_k = max(0, T₀ - 0.2×k) (faster cooling)

**2-opt Move:**
```
Before: A---B...C---D
After:  A---C...B---D (reverse middle segment)
```

---

### 2: Tile Shatter Game
```
Input:  [3, 1, 5, 8]
Output: 167
Method: Bottom-up DP (O(N³))
```

**Key Function:**
```python
max_shatter_points(tile_multipliers) → int
```

**Recurrence:**
```
dp[i][j] = max points shattering tiles between i and j
dp[i][j] = max(
    dp[i][k] + dp[k][j] + tiles[i]×tiles[k]×tiles[j]
    for k in range(i+1, j)
)
```

**Test Cases:**
- [3,1,5,8] → 167 ✓
- [1,5] → 10 ✓

---

### 3: Minimum Service Centers
```
Input:  Binary tree as level-order list
        [0, 0, None, 0, None, 0, None, None, 0]
Output: 2 (minimum centers needed)
Method: Post-order DFS with states 0/1/2
```

**Key Function:**
```python
min_service_centers(root) → int
build_tree_from_level_list(level_list) → TreeNode
```

**State Definition:**
| State | Meaning | Placement |
|-------|---------|-----------|
| 0 | Not covered | Need parent center |
| 1 | Has center | Covers neighbors |
| 2 | Covered | By child/parent center |

**Logic:**
```python
if child == 0: place center here → return 1
elif child == 1: covered by child → return 2
else: not covered → return 0
```

---

### 4: Energy Grid Distribution
```
Input:  Hourly district demands + source availability
Output: Allocation plan + cost analysis
Method: Greedy (prioritize cheap renewables)
```

**Key Functions:**
```python
process_all_hours(demand_dict, sources) → results
allocate_energy_by_source(available_sources, district_demands) → (allocation, energy, cost)
```

**Source Priority:**
1. **Solar** (Cost: Rs. 1.0/kWh, 6-18h)
2. **Hydro** (Cost: Rs. 1.5/kWh, 0-24h)
3. **Diesel** (Cost: Rs. 3.0/kWh, 17-23h) ← Last resort

**Demand Tolerance:** 0.9 ≤ (energy_used / demand) ≤ 1.1

---

### 5A: Emergency Network Simulator
```
Input:  8-node weighted graph
Output: MST, disjoint paths, BST optimization, coloring
Method: Kruskal's, Dijkstra, Welsh-Powell
UI:     Tkinter with network visualization
```

**Key Functions:**
```python
_compute_mst()           # Kruskal's algorithm
_find_disjoint_paths()   # Suurballe's algorithm
_optimize_bst()          # DSW rebalancing
_apply_graph_coloring()  # Welsh-Powell
```

**Operations:**
| Button | Algorithm | Result |
|--------|-----------|--------|
| Q1: Compute MST | Kruskal | Green edges |
| Q2: Find Disjoint Paths | Suurballe | Orange edges |
| Q3: Optimize BST | DSW | Height reduced |
| Q4: Simulate Failure | Mark node | Gray node |
| Graph Coloring | Welsh-Powell | 3-4 colors |

---

### 5B: Multithreaded Sorting
```
Input:  Integer array (comma/space separated)
Output: Sorted array + thread logs
Method: QuickSort with 3 threads (left, right, merge)
UI:     Tkinter with thread status log
```

**Key Functions:**
```python
class SortingSystem:
  quicksort(arr, low, high) → None
  _partition(arr, low, high) → int
  start_sorting(data) → None
  wait_for_completion() → sorted_list
```

**Thread Structure:**
```
     Left Thread       Right Thread
    (quicksort)      (quicksort)
           ↓                ↓
           └──► Merge Thread ◄──┘
              (waits + merges)
                        ↓
                  Sorted Result
```

**Thread Log Example:**
```
[1] SYSTEM: Received 10 elements: [5, 2, 8, ...]
[2] SYSTEM: Split into halves - Left: [5,2], Right: [8,...]
[3] THREAD_LEFT: Starting to sort left half
[4] THREAD_RIGHT: Starting to sort right half
[5] THREAD_MERGE: Waiting for sorting threads...
[6] THREAD_MERGE: All threads completed, starting merge...
[7] THREAD_MERGE: Completed. Final result: [2, 5, 8, ...]
```

---

### 6: Robot Delivery Pathfinding
```
Start:  Glogow (Blue)
Goal:   Plock (Red)
Graph:  13 Polish cities with weighted edges
Methods: DFS, BFS, A* comparison
```

**Key Functions:**
```python
depth_first_search() → (path, nodes_explored, steps)
breadth_first_search() → (path, nodes_explored, steps)
a_star_search() → (path, nodes_explored, steps)
generate_comparative_report(dfs, bfs, astar)
```

**Algorithm Comparison:**

| Algorithm | Optimal | Time | Space | Use Case |
|-----------|---------|------|-------|----------|
| DFS | ✗ | O(V+E) | O(h) | Deep exploration |
| BFS | ✓* | O(V+E) | O(V) | Shortest unweighted |
| A* | ✓** | O(b^d) | O(b^d) | **Best for weighted** |

*Unweighted graphs only  
**With admissible heuristic

**A* Formula:**
```
f(n) = g(n) + h(n)
where:
  g(n) = actual cost from start (Glogow)
  h(n) = straight-line distance to goal (Plock)
```

**Step Output Example:**
```
Step 1:
  Current City: Glogow
  Open Set: ['Poznań', 'Zielona_Gora', 'Wroclaw']
  Closed Set: set()

Step 2:
  Current City: Poznań
  Open Set: ['Wroclaw', 'Konin', 'Lodz', 'Zielona_Gora']
  Closed Set: {'Glogow'}
```

---

## 🚀 Quick Start

### Running GUI Applications
```bash
# Network Simulator (5 major operations)
python Task5a.py

# Multithreaded Sorting (watch thread logs)
python Task5b.py
```

### Running Console Applications
```bash
# Weiszfeld (test 2 cases)
python Task1a.py

# TSP (compare cooling schedules)
python Task1b.py

# Tile Shatter (validate DP solution)
python Task2.py

# Min Centers (tree construction demo)
python Task3.py

# Energy Grid (hourly allocation report)
python Task4.py

# Robot Delivery (all 3 algorithms comparison)
python Task6.py
```

---

## 📊 Complexity At-A-Glance

```
Weiszfeld:      O(I×N)        Space: O(N)       ✓ Optimal
TSP:            O(M×N²)       Space: O(N)       ~ Approximate
Tile Shatter:   O(N³)         Space: O(N²)      ✓ Optimal
Min Centers:    O(N)          Space: O(H)       ✓ Optimal
Energy Grid:    O(H×S×D)      Space: O(H×D)     ✓ Feasible
Network Sim:    O(E log E)    Space: O(V)       ✓ Optimal
MergeSort:      O(N log N)    Space: O(N)       ✓ Optimal
Pathfinding:    varies        varies            varies
└─ DFS:         O(V+E)        O(H)              ✗ Not optimal
└─ BFS:         O(V+E)        O(V)              ✓ Optimal (unweighted)
└─ A*:          O(b^d)        O(b^d)            ✓ Optimal (with heuristic)
```

---

## 🎯 Test Results Summary

| Problem | Status | Notes |
|---------|--------|-------|
| Weiszfeld | ✓ 2/2 | Both test cases pass |
| TSP | ✓ Visual | Empirical optimization verified |
| Tile Shatter | ✓ 2/2 | DP correctness proven |
| Min Centers | ✓ 2/2 | Tree logic validated |
| Energy Grid | ✓ 8h×3d | All hours within tolerance |
| Network Sim | ✓ 5 ops | All operations display correctly |
| Multithreaded | ✓ Param | Thread safety verified |
| Pathfinding | ✓ 3 algo | All algorithms find paths |

---

## 💡 Tips for Viva Preparation

### Weiszfeld
- Explain why inverse distance weighting works
- Discuss convergence criterion (1e-7)
- Be ready to justify iterations (100)

### TSP
- Explain 2-opt move concept
- Compare exponential vs linear cooling
- Discuss local minima escape mechanism

### Tile Shatter
- Draw recurrence relation on board
- Explain why O(N³) (3 nested loops)
- Prove optimal substructure

### Min Centers
- Explain post-order traversal benefit
- Justify state 0/1/2 definitions
- Discuss boundary (null nodes as state 2)

### Energy Grid
- Explain greedy choice property
- Discuss source priority reasoning
- Verify ±10% demand tolerance

### Network Sim
- Explain Kruskal's union-find
- Discuss Suurballe's dual paths
- BST rebalancing (height improvement)

### Multithreaded Sort
- Explain join() synchronization
- Discuss thread safety (locks)
- Time complexity (still O(n log n) despite threads)

### Pathfinding
- Compare all 3 algorithms side-by-side
- Explain f(n) = g(n) + h(n) formula
- Justify why A* is best for weighted graphs

---

## 📌 Key Files Reference

```
question1a.py  → compute_optimal_hub_location()
question1b.py  → simulated_annealing()
question2.py   → max_shatter_points()
question3.py   → min_service_centers(), build_tree_from_level_list()
question4.py   → process_all_hours()
question5a.py  → SimulatorGUI class (GUI)
question5b.py  → SortingCoordinator class (GUI)
question6.py   → depth_first_search(), breadth_first_search(), a_star_search()
```

---

**Last Updated:** 25 January 2026  
**Module:** ST5003CEM Advanced Algorithms