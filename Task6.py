"""
Robot Delivery Path Finding - Functional Approach
Pure functions for DFS, BFS, and A* with immutable data structures.
Emphasizes composition, pure functions, and functional data handling.
"""

from collections import deque
import heapq
from typing import Tuple, List, Dict, Optional, Set


# ======================== GRAPH DATA ========================

CITY_GRAPH = {
    'Glogow': {'Zielona_Gora': 50, 'Poznan': 85, 'Wroclaw': 120},
    'Zielona_Gora': {'Glogow': 50, 'Poznan': 60, 'Szczecin': 180},
    'Poznan': {'Glogow': 85, 'Zielona_Gora': 60, 'Wroclaw': 90, 'Konin': 70, 'Lodz': 110},
    'Wroclaw': {'Glogow': 120, 'Poznan': 90, 'Opole': 95, 'Kalisz': 130},
    'Szczecin': {'Zielona_Gora': 180, 'Gdansk': 350},
    'Konin': {'Poznan': 70, 'Lodz': 95, 'Warsaw': 180},
    'Lodz': {'Poznan': 110, 'Konin': 95, 'Warsaw': 140, 'Plock': 150},
    'Warsaw': {'Konin': 180, 'Lodz': 140, 'Plock': 120, 'Radom': 100},
    'Plock': {'Lodz': 150, 'Warsaw': 120},
    'Opole': {'Wroclaw': 95, 'Kalisz': 120},
    'Kalisz': {'Wroclaw': 130, 'Opole': 120, 'Lodz': 80},
    'Radom': {'Warsaw': 100},
    'Gdansk': {'Szczecin': 350},
}

HEURISTIC_DISTANCES = {
    'Glogow': 380, 'Zielona_Gora': 400, 'Poznan': 340, 'Wroclaw': 450,
    'Szczecin': 500, 'Konin': 280, 'Lodz': 150, 'Warsaw': 120, 'Plock': 0,
    'Opole': 480, 'Kalisz': 200, 'Radom': 140, 'Gdansk': 550,
}

START_CITY = 'Glogow'
GOAL_CITY = 'Plock'


# ======================== PURE UTILITY FUNCTIONS ========================

def get_neighbors(city: str, graph: Dict) -> List[Tuple[str, int]]:
    """Get list of (neighbor, distance) tuples for a city."""
    return [(n, d) for n, d in graph.get(city, {}).items()]


def is_goal(city: str, goal: str) -> bool:
    """Check if city is the goal."""
    return city == goal


def reconstruct_path_from_parents(parents: Dict[str, Optional[str]], goal: str) -> List[str]:
    """Reconstruct path from parent dictionary."""
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parents.get(current)
    return list(reversed(path))


def calculate_path_cost(path: List[str], graph: Dict) -> int:
    """Calculate total cost of a path."""
    return sum(
        graph.get(path[i], {}).get(path[i+1], 0)
        for i in range(len(path) - 1)
    )


def format_step_output(step: int, current: str, open_set: List, closed_set: Set, extra: str = "") -> str:
    """Format step information for display."""
    output = f"\nStep {step}:\n"
    output += f"  Current City: {current}\n"
    output += f"  Open Set: {open_set}\n"
    output += f"  Closed Set: {closed_set}\n"
    if extra:
        output += extra
    return output


# ======================== DFS IMPLEMENTATION ========================

def dfs_search_step(
    current: str,
    open_stack: List[str],
    closed_set: Set[str],
    parents: Dict[str, Optional[str]],
    graph: Dict,
    step: int,
    goal: str
) -> Tuple[bool, List[str], int, List[str], Set[str], Dict]:
    """
    Single step of DFS search.
    Returns: (found, path, new_step, new_open, new_closed, new_parents)
    """
    print(f"\nStep {step}:")
    print(f"  Current City: {current}")
    print(f"  Open Set: {open_stack}")
    print(f"  Closed Set: {closed_set}")
    
    if is_goal(current, goal):
        path = reconstruct_path_from_parents(parents, current)
        return True, path, step, [], closed_set, parents
    
    new_closed = closed_set | {current}
    new_open = open_stack.copy()
    new_parents = parents.copy()
    
    for neighbor, _ in reversed(get_neighbors(current, graph)):
        if neighbor not in new_closed and neighbor not in new_open:
            new_open.append(neighbor)
            new_parents[neighbor] = current
            print(f"  Adding to Open: {neighbor} (parent: {current})")
    
    return False, [], step, new_open, new_closed, new_parents


def dfs_search(start: str, goal: str, graph: Dict) -> Tuple[Optional[List[str]], int, int]:
    """
    Depth-First Search using functional recursion pattern.
    Returns: (path, nodes_explored, steps_taken)
    """
    print("\n" + "="*80)
    print("DEPTH-FIRST SEARCH (DFS) - FUNCTIONAL")
    print("="*80)
    
    def dfs_loop(open_stack: List[str], closed_set: Set[str], 
                 parents: Dict[str, Optional[str]], step: int) -> Tuple[Optional[List[str]], int, int]:
        """Recursive DFS loop."""
        if not open_stack:
            return None, len(closed_set), step
        
        current = open_stack.pop()
        
        found, path, _, new_open, new_closed, new_parents = dfs_search_step(
            current, open_stack, closed_set, parents, graph, step, goal
        )
        
        if found:
            return path, len(new_closed), step
        
        return dfs_loop(new_open, new_closed, new_parents, step + 1)
    
    path, explored, steps = dfs_loop([start], set(), {start: None}, 1)
    
    if path:
        print(f"\n✓ GOAL FOUND: {goal}")
    
    return path, explored, steps


# ======================== BFS IMPLEMENTATION ========================

def bfs_search(start: str, goal: str, graph: Dict) -> Tuple[Optional[List[str]], int, int]:
    """
    Breadth-First Search using functional composition.
    Returns: (path, nodes_explored, steps_taken)
    """
    print("\n" + "="*80)
    print("BREADTH-FIRST SEARCH (BFS) - FUNCTIONAL")
    print("="*80)
    
    def bfs_loop(open_queue: deque, closed_set: Set[str], 
                 parents: Dict[str, Optional[str]], step: int) -> Tuple[Optional[List[str]], int, int]:
        """Recursive BFS loop with queue."""
        if not open_queue:
            return None, len(closed_set), step
        
        current = open_queue.popleft()
        
        print(f"\nStep {step}:")
        print(f"  Current City: {current}")
        print(f"  Open Set: {list(open_queue)}")
        print(f"  Closed Set: {closed_set}")
        
        if is_goal(current, goal):
            path = reconstruct_path_from_parents(parents, current)
            print(f"\n✓ GOAL FOUND: {goal}")
            return path, len(closed_set | {current}), step
        
        new_closed = closed_set | {current}
        new_queue = deque(open_queue)
        new_parents = parents.copy()
        
        for neighbor, _ in get_neighbors(current, graph):
            if neighbor not in new_closed and neighbor not in new_queue:
                new_queue.append(neighbor)
                new_parents[neighbor] = current
                print(f"  Adding to Open: {neighbor} (parent: {current})")
        
        return bfs_loop(new_queue, new_closed, new_parents, step + 1)
    
    path, explored, steps = bfs_loop(deque([start]), set(), {start: None}, 1)
    return path, explored, steps


# ======================== A* IMPLEMENTATION ========================

def calculate_f_score(g_score: int, h_score: int) -> int:
    """Calculate f(n) = g(n) + h(n)."""
    return g_score + h_score


def expand_node(
    current: str,
    g_scores: Dict[str, int],
    heuristic: Dict[str, int],
    graph: Dict
) -> List[Tuple[int, str]]:
    """
    Generate f-scores for neighbors.
    Returns list of (f_score, neighbor).
    """
    neighbors = []
    for neighbor, edge_cost in get_neighbors(current, graph):
        new_g = g_scores[current] + edge_cost
        h = heuristic.get(neighbor, float('inf'))
        f = calculate_f_score(new_g, h)
        neighbors.append((f, neighbor, new_g))
    return neighbors


def astar_search(start: str, goal: str, graph: Dict, heuristic: Dict) -> Tuple[Optional[List[str]], int, int]:
    """
    A* Search using functional composition with priority queue.
    Returns: (path, nodes_explored, steps_taken)
    """
    print("\n" + "="*80)
    print("A* SEARCH - FUNCTIONAL")
    print("="*80)
    
    counter = 0
    open_heap = [(heuristic[start], counter, start)]
    counter += 1
    
    g_scores = {start: 0}
    closed_set = set()
    parents = {start: None}
    step = 1
    
    while open_heap:
        f_score, _, current = heapq.heappop(open_heap)
        
        if current in closed_set:
            continue
        
        open_cities = [c for _, _, c in open_heap]
        
        print(f"\nStep {step}:")
        print(f"  Current City: {current}")
        print(f"  f(n) = g(n) + h(n) = {g_scores[current]} + {heuristic[current]} = {f_score}")
        print(f"  Open Set: {open_cities}")
        print(f"  Closed Set: {closed_set}")
        
        if is_goal(current, goal):
            path = reconstruct_path_from_parents(parents, current)
            print(f"\n✓ GOAL FOUND: {goal}")
            return path, len(closed_set) + 1, step
        
        closed_set.add(current)
        
        for f_val, neighbor, new_g in expand_node(current, g_scores, heuristic, graph):
            if neighbor not in closed_set:
                if neighbor not in g_scores or new_g < g_scores[neighbor]:
                    g_scores[neighbor] = new_g
                    parents[neighbor] = current
                    heapq.heappush(open_heap, (f_val, counter, neighbor))
                    counter += 1
                    print(f"  Adding/Updating {neighbor}: g={new_g}, h={heuristic[neighbor]}, f={f_val}")
        
        step += 1
    
    return None, len(closed_set), step


# ======================== REPORT GENERATION ========================

def generate_comparison_report(
    results: Dict[str, Tuple[Optional[List[str]], int, int]]
) -> None:
    """Generate functional comparative analysis report."""
    print("\n" + "="*80)
    print("COMPARATIVE ANALYSIS REPORT")
    print("="*80)
    
    dfs_path, dfs_explored, dfs_steps = results['DFS']
    bfs_path, bfs_explored, bfs_steps = results['BFS']
    astar_path, astar_explored, astar_steps = results['A*']
    
    for algo, path, explored, steps in [
        ('DFS', dfs_path, dfs_explored, dfs_steps),
        ('BFS', bfs_path, bfs_explored, bfs_steps),
        ('A*', astar_path, astar_explored, astar_steps),
    ]:
        print(f"\n{algo}:")
        if path:
            cost = calculate_path_cost(path, CITY_GRAPH)
            print(f"  Path: {' -> '.join(path)}")
            print(f"  Cost: {cost} km, Length: {len(path)-1} edges")
        else:
            print(f"  No path found")
        print(f"  Nodes Explored: {explored}, Steps: {steps}")
    
    # Optimality check
    if astar_path and bfs_path:
        astar_cost = calculate_path_cost(astar_path, CITY_GRAPH)
        bfs_cost = calculate_path_cost(bfs_path, CITY_GRAPH)
        print(f"\nOptimality: A* {'≤' if astar_cost <= bfs_cost else '>'} BFS")
    
    print("\nRecommendation: Use A* for robot delivery (optimal with good heuristic)")


# ======================== MAIN EXECUTION ========================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("ROBOT DELIVERY PATHFINDING - FUNCTIONAL APPROACH")
    print(f"Start: {START_CITY} → Goal: {GOAL_CITY}")
    print("="*80)
    
    results = {
        'DFS': dfs_search(START_CITY, GOAL_CITY, CITY_GRAPH),
        'BFS': bfs_search(START_CITY, GOAL_CITY, CITY_GRAPH),
        'A*': astar_search(START_CITY, GOAL_CITY, CITY_GRAPH, HEURISTIC_DISTANCES),
    }
    
    generate_comparison_report(results)
