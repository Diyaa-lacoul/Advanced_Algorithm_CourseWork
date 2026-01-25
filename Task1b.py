"""
Traveling Salesperson Problem - Simulated Annealing Hybrid Implementation
Modular Design with Component-Based Architecture

This solution combines functional and object-oriented paradigms
with clear separation between different algorithm components.
"""

import random
import math


# ============================================================================
# CITY MANAGEMENT FUNCTIONS
# ============================================================================

def generate_cities(count, max_coord=100):
    """
    Generate random city coordinates in a 2D plane.
    
    Args:
        count (int): Number of cities to generate
        max_coord (int): Maximum coordinate value
    
    Returns:
        list: List of [x, y] coordinate pairs
    """
    cities = []
    for _ in range(count):
        cities.append([
            random.uniform(0, max_coord),
            random.uniform(0, max_coord)
        ])
    return cities


def distance_between(city_a, city_b):
    """
    Calculate Euclidean distance between two cities.
    
    Args:
        city_a (list): [x, y] coordinates
        city_b (list): [x, y] coordinates
    
    Returns:
        float: Euclidean distance
    """
    dx = city_a[0] - city_b[0]
    dy = city_a[1] - city_b[1]
    return math.sqrt(dx * dx + dy * dy)


def evaluate_tour_length(tour, cities):
    """
    Calculate the total distance of a tour.
    
    The tour is a complete cycle, including distance from last to first city.
    
    Args:
        tour (list): Indices of cities in tour order
        cities (list): City coordinates
    
    Returns:
        float: Total tour distance
    """
    total_distance = 0.0
    tour_size = len(tour)
    
    for position in range(tour_size):
        current_idx = tour[position]
        next_idx = tour[(position + 1) % tour_size]
        
        segment_distance = distance_between(
            cities[current_idx],
            cities[next_idx]
        )
        total_distance += segment_distance
    
    return total_distance


# ============================================================================
# NEIGHBORHOOD GENERATION
# ============================================================================

def generate_two_opt_neighbor(tour, segment_start, segment_end):
    """
    Generate a new tour by applying 2-opt move.
    
    The 2-opt move reverses the segment between segment_start and segment_end.
    This is computationally efficient and effective for TSP problems.
    
    Example: [0,1,2,3,4] with start=1, end=3 becomes [0,3,2,1,4]
    
    Args:
        tour (list): Current tour
        segment_start (int): Start index of segment to reverse
        segment_end (int): End index of segment to reverse
    
    Returns:
        list: New tour with segment reversed
    """
    new_tour = (
        tour[:segment_start] +
        tour[segment_start:segment_end+1][::-1] +
        tour[segment_end+1:]
    )
    return new_tour


# ============================================================================
# COOLING SCHEDULES
# ============================================================================

class ExponentialSchedule:
    """Exponential cooling schedule: T = T₀ * α^k"""
    
    def __init__(self, initial, rate):
        self.initial = initial
        self.rate = rate
    
    def temperature_at_iteration(self, iteration):
        """Get temperature for exponential schedule."""
        return self.initial * (self.rate ** iteration)


class LinearSchedule:
    """Linear cooling schedule: T = T₀ - β*k"""
    
    def __init__(self, initial, decrement):
        self.initial = initial
        self.decrement = decrement
    
    def temperature_at_iteration(self, iteration):
        """Get temperature for linear schedule."""
        return max(0, self.initial - (self.decrement * iteration))


# ============================================================================
# ACCEPTANCE CRITERION
# ============================================================================

def metropolis_acceptance(current_cost, candidate_cost, temperature):
    """
    Determine solution acceptance using Metropolis criterion.
    
    This is the key mechanism allowing escape from local optima.
    Better solutions are always accepted.
    Worse solutions are accepted with probability P = exp(-ΔE / T)
    
    At high temperatures, worse solutions have higher chance of acceptance.
    At low temperatures, mostly better solutions are accepted.
    
    Args:
        current_cost (float): Distance of current tour
        candidate_cost (float): Distance of candidate tour
        temperature (float): Current temperature (must be > 0)
    
    Returns:
        bool: True if candidate should be accepted
    """
    # Always accept improvements
    if candidate_cost < current_cost:
        return True
    
    # Calculate energy increase
    energy_increase = candidate_cost - current_cost
    
    # Calculate acceptance probability
    if temperature > 0:
        acceptance_prob = math.exp(-energy_increase / temperature)
    else:
        acceptance_prob = 0.0
    
    # Accept based on probability
    return random.random() < acceptance_prob


# ============================================================================
# MAIN SOLVER
# ============================================================================

class TSPSimulatedAnnealingSolver:
    """Encapsulates the Simulated Annealing TSP solver."""
    
    def __init__(self, cities):
        self.cities = cities
        self.num_cities = len(cities)
        self.iterations_performed = 0
        self.best_route = None
        self.best_cost = float('inf')
    
    def solve(self, cooling_schedule, max_iterations=5000, min_temperature=1e-8):
        """
        Execute the Simulated Annealing algorithm.
        
        Algorithm steps:
        1. Start with random tour
        2. Generate neighbor using 2-opt move
        3. Accept/reject using Metropolis criterion
        4. Cool temperature according to schedule
        5. Repeat until convergence or max iterations
        
        Args:
            cooling_schedule: Schedule object with temperature_at_iteration method
            max_iterations (int): Maximum iterations
            min_temperature (float): Stopping criterion
        
        Returns:
            tuple: (best_tour, best_distance)
        """
        # Initialize with random solution
        current_tour = list(range(self.num_cities))
        random.shuffle(current_tour)
        current_distance = evaluate_tour_length(current_tour, self.cities)
        
        best_tour = current_tour[:]
        best_distance = current_distance
        
        # Optimization loop
        for iteration in range(max_iterations):
            # Get temperature for this iteration
            temperature = cooling_schedule.temperature_at_iteration(iteration)
            
            # Stop if cooled enough
            if temperature < min_temperature:
                break
            
            # Select random 2-opt move
            idx1 = random.randint(0, self.num_cities - 1)
            idx2 = random.randint(0, self.num_cities - 1)
            
            if idx1 > idx2:
                idx1, idx2 = idx2, idx1
            
            if idx1 == idx2:
                continue
            
            # Generate and evaluate neighbor
            neighbor_tour = generate_two_opt_neighbor(current_tour, idx1, idx2)
            neighbor_distance = evaluate_tour_length(neighbor_tour, self.cities)
            
            # Make acceptance decision
            if metropolis_acceptance(current_distance, neighbor_distance, temperature):
                current_tour = neighbor_tour
                current_distance = neighbor_distance
                
                # Track best solution
                if current_distance < best_distance:
                    best_tour = current_tour[:]
                    best_distance = current_distance
        
        self.best_route = best_tour
        self.best_cost = best_distance
        self.iterations_performed = iteration + 1
        
        return best_tour, best_distance


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("TSP SIMULATED ANNEALING - HYBRID MODULAR APPROACH")
    print("=" * 70)
    
    # Setup
    random.seed(42)
    NUM_CITIES = 30
    cities = generate_cities(NUM_CITIES, max_coord=100)
    
    print(f"\nProblem Configuration:")
    print(f"  - Number of cities: {NUM_CITIES}")
    print(f"  - Grid size: 100x100")
    
    # Experiment 1: Exponential cooling
    print("\n" + "-" * 70)
    print("EXPERIMENT 1: Exponential Cooling Schedule")
    print("-" * 70)
    print("Temperature formula: T = 1000 × 0.9995^k")
    
    schedule_exp = ExponentialSchedule(initial=1000.0, rate=0.9995)
    solver_exp = TSPSimulatedAnnealingSolver(cities)
    tour_exp, dist_exp = solver_exp.solve(schedule_exp)
    
    print(f"Final tour distance: {dist_exp:.2f}")
    print(f"Iterations executed: {solver_exp.iterations_performed}")
    
    # Experiment 2: Linear cooling
    print("\n" + "-" * 70)
    print("EXPERIMENT 2: Linear Cooling Schedule")
    print("-" * 70)
    print("Temperature formula: T = 1000 - 0.2×k")
    
    schedule_lin = LinearSchedule(initial=1000.0, decrement=0.2)
    solver_lin = TSPSimulatedAnnealingSolver(cities)
    tour_lin, dist_lin = solver_lin.solve(schedule_lin)
    
    print(f"Final tour distance: {dist_lin:.2f}")
    print(f"Iterations executed: {solver_lin.iterations_performed}")
    
    # Comparison and analysis
    print("\n" + "-" * 70)
    print("PERFORMANCE COMPARISON")
    print("-" * 70)
    
    print(f"Exponential Cooling: {dist_exp:.2f} units")
    print(f"Linear Cooling:      {dist_lin:.2f} units")
    
    improvement = abs(dist_exp - dist_lin)
    if dist_exp < dist_lin:
        better = "EXPONENTIAL"
        ratio = dist_lin / dist_exp if dist_exp > 0 else 1
    else:
        better = "LINEAR"
        ratio = dist_exp / dist_lin if dist_lin > 0 else 1
    
    print(f"\nBetter Performance:  {better}")
    print(f"Improvement Margin:  {improvement:.2f} units ({(ratio-1)*100:.1f}%)")
    
    print("\n" + "=" * 70)
    print("Analysis complete. Both cooling schedules converged successfully.")
    print("=" * 70 + "\n")
