"""
Sensor Hub Optimization - Simplified Weiszfeld Algorithm
Clean, easy-to-understand implementation for educational purposes

This code finds the optimal hub location that minimizes total distance to all sensors.
It uses the Weiszfeld iterative method to locate the geometric median.
"""

import math


def distance_between_points(point1, point2):
    """
    Calculate Euclidean distance between two 2D points.
    
    Args:
        point1: [x, y] coordinates of first point
        point2: [x, y] coordinates of second point
    
    Returns:
        float: The Euclidean distance
    """
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    return math.sqrt(dx * dx + dy * dy)


def calculate_initial_hub(sensors):
    """
    Initialize hub position at the centroid (average) of all sensors.
    
    Args:
        sensors: List of [x, y] sensor coordinates
    
    Returns:
        list: [hub_x, hub_y] at centroid position
    """
    sum_x = 0
    sum_y = 0
    
    for sensor in sensors:
        sum_x = sum_x + sensor[0]
        sum_y = sum_y + sensor[1]
    
    hub_x = sum_x / len(sensors)
    hub_y = sum_y / len(sensors)
    
    return [hub_x, hub_y]


def weiszfeld_optimization(sensors):
    """
    Apply Weiszfeld algorithm to find the optimal hub location.
    
    The algorithm iteratively moves the hub to minimize total distance:
    1. Start with hub at centroid
    2. For each iteration, calculate inverse-distance weights for each sensor
    3. Move hub to weighted average position
    4. Repeat until convergence
    
    Args:
        sensors: List of [x, y] sensor coordinates
    
    Returns:
        list: [optimal_hub_x, optimal_hub_y]
    """
    
    # Step 1: Initialize hub at centroid
    current_hub = calculate_initial_hub(sensors)
    
    # Step 2: Set optimization parameters
    max_iterations = 100
    convergence_threshold = 1e-7
    min_distance = 1e-10  # Prevent division by zero
    
    # Step 3: Iterative refinement
    for iteration in range(max_iterations):
        # Store previous hub to check convergence
        previous_hub = [current_hub[0], current_hub[1]]
        
        # Calculate weighted sum
        weighted_x = 0
        weighted_y = 0
        total_weight = 0
        
        # For each sensor, calculate its contribution based on inverse distance
        for sensor in sensors:
            # Calculate distance from current hub to this sensor
            dist = distance_between_points(current_hub, sensor)
            
            # Handle case where hub is exactly on a sensor
            if dist < min_distance:
                dist = min_distance
            
            # Weight is inverse of distance (closer sensors have higher weight)
            weight = 1.0 / dist
            
            # Accumulate weighted sensor positions
            weighted_x = weighted_x + weight * sensor[0]
            weighted_y = weighted_y + weight * sensor[1]
            total_weight = total_weight + weight
        
        # Calculate new hub position as weighted average
        current_hub[0] = weighted_x / total_weight
        current_hub[1] = weighted_y / total_weight
        
        # Check if hub has converged (movement is very small)
        hub_movement = distance_between_points(current_hub, previous_hub)
        
        if hub_movement < convergence_threshold:
            break  # Convergence reached, stop iterations
    
    return current_hub


def calculate_total_distance(hub, sensors):
    """
    Calculate the total distance from hub to all sensors.
    
    Args:
        hub: [hub_x, hub_y] position
        sensors: List of [x, y] sensor coordinates
    
    Returns:
        float: Sum of distances from hub to all sensors
    """
    total = 0
    
    for sensor in sensors:
        dist = distance_between_points(hub, sensor)
        total = total + dist
    
    return total


def find_optimal_hub(sensor_locations):
    """
    Main function to solve the optimal sensor placement problem.
    
    Args:
        sensor_locations: List of [x, y] sensor coordinates
    
    Returns:
        float: Minimum total distance
    """
    
    # Handle edge cases
    if len(sensor_locations) == 0:
        raise ValueError("No sensors provided")
    
    if len(sensor_locations) == 1:
        return 0.0
    
    # Find optimal hub using Weiszfeld algorithm
    optimal_hub = weiszfeld_optimization(sensor_locations)
    
    # Calculate and return total distance
    result = calculate_total_distance(optimal_hub, sensor_locations)
    
    return round(result, 5)


# Test and Validation Section
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SENSOR HUB OPTIMIZATION - SIMPLIFIED WEISZFELD")
    print("=" * 60)
    
    # Test Case 1: Four sensors arranged in a square
    print("\nTest Case 1: Square Configuration")
    print("-" * 60)
    
    sensors_case1 = [[0, 1], [1, 0], [1, 2], [2, 1]]
    result_case1 = find_optimal_hub(sensors_case1)
    expected_case1 = 4.0
    
    print(f"Sensor Locations: {sensors_case1}")
    print(f"Calculated Result: {result_case1}")
    print(f"Expected Result:   {expected_case1}")
    
    test_pass1 = abs(result_case1 - expected_case1) < 0.01
    print(f"Test Status: {'PASS' if test_pass1 else 'FAIL'}")
    
    # Test Case 2: Two sensors on a diagonal
    print("\nTest Case 2: Diagonal Pair Configuration")
    print("-" * 60)
    
    sensors_case2 = [[1, 1], [3, 3]]
    result_case2 = find_optimal_hub(sensors_case2)
    expected_case2 = 2.82843
    
    print(f"Sensor Locations: {sensors_case2}")
    print(f"Calculated Result: {result_case2}")
    print(f"Expected Result:   {expected_case2}")
    
    test_pass2 = abs(result_case2 - expected_case2) < 0.01
    print(f"Test Status: {'PASS' if test_pass2 else 'FAIL'}")
    
    print("\n" + "=" * 60)
    print("Summary: Both tests passed!" if test_pass1 and test_pass2 else "Summary: Some tests failed")
    print("=" * 60 + "\n")
