"""
Strategic Tile Shatter Game - Modular Functional Approach
Helper Functions with Clean Separation of Concerns

This solution uses separate utility functions for initialization,
computation, and result extraction to improve readability.
"""


def prepare_tile_array(multipliers):
    """
    Pre-process tile multipliers by adding boundary values.
    
    The boundaries (1) help calculate edge cases where a tile
    has no left or right neighbor naturally.
    
    Args:
        multipliers (list): Original tile multiplier values
    
    Returns:
        list: Modified array with boundaries [1] + multipliers + [1]
    """
    return [1] + multipliers + [1]


def initialize_dp_table(size):
    """
    Create empty DP table for dynamic programming.
    
    Args:
        size (int): Size of the tile array (including boundaries)
    
    Returns:
        list: 2D list initialized with zeros
    """
    return [[0] * size for _ in range(size)]


def calculate_points_for_configuration(tiles, dp, left_bound, right_bound, last_shatter_idx):
    """
    Calculate total points if tile at last_shatter_idx is shattered last
    in the range between left_bound and right_bound.
    
    When tile at last_shatter_idx is shattered last:
    - Its immediate neighbors are tiles[left_bound] and tiles[right_bound]
    - Points for this action = tiles[left_bound] * tiles[last_shatter_idx] * tiles[right_bound]
    - Plus all points from the left subrange and right subrange
    
    Args:
        tiles (list): Array of tile multipliers with boundaries
        dp (list): DP table with previously computed results
        left_bound (int): Left boundary of the current range
        right_bound (int): Right boundary of the current range
        last_shatter_idx (int): Index of tile to shatter last
    
    Returns:
        int: Total points from this configuration
    """
    # Get points already computed for left side
    left_subrange_points = dp[left_bound][last_shatter_idx]
    
    # Get points already computed for right side
    right_subrange_points = dp[last_shatter_idx][right_bound]
    
    # Calculate points for shattering this tile last
    shattering_this_tile = tiles[left_bound] * tiles[last_shatter_idx] * tiles[right_bound]
    
    # Sum all components
    total = left_subrange_points + right_subrange_points + shattering_this_tile
    
    return total


def fill_dp_table(tiles, dp):
    """
    Fill the DP table using bottom-up approach.
    
    Build solution from smaller subproblems to larger ones.
    For each range, find the best tile to shatter last.
    
    Args:
        tiles (list): Array of tile multipliers with boundaries
        dp (list): DP table to be filled
    """
    n = len(tiles)
    
    # Iterate by range length (distance between left and right indices)
    for range_len in range(2, n):
        # For each valid left index
        for left_idx in range(n - range_len):
            # Calculate right index
            right_idx = left_idx + range_len
            
            # Try each possible tile to shatter last
            for middle_idx in range(left_idx + 1, right_idx):
                # Get points for this configuration
                candidate_points = calculate_points_for_configuration(
                    tiles, dp, left_idx, right_idx, middle_idx
                )
                
                # Keep the maximum
                dp[left_idx][right_idx] = max(dp[left_idx][right_idx], candidate_points)


def extract_result(dp):
    """
    Extract the final answer from the completed DP table.
    
    The answer is at dp[0][n-1] where 0 and n-1 are the boundaries.
    
    Args:
        dp (list): Completed DP table
    
    Returns:
        int: Maximum points achievable
    """
    n = len(dp)
    return dp[0][n - 1]


def max_shatter_points(tile_multipliers):
    """
    Calculate maximum points from shattering tiles optimally.
    
    Uses dynamic programming where:
    - dp[i][j] = max points from shattering all tiles between i and j
    - Recurrence: Try each tile as last to shatter and pick best
    
    Time Complexity: O(n^3)
    
    
    Args:
        tile_multipliers (list): Multiplier value for each tile
    
    Returns:
        int: Maximum total points
    """
    # Handle edge cases
    if not tile_multipliers or len(tile_multipliers) == 1:
        return 0
    
    # Step 1: Prepare the tile array with boundaries
    tiles = prepare_tile_array(tile_multipliers)
    
    # Step 2: Initialize the DP table
    dp = initialize_dp_table(len(tiles))
    
    # Step 3: Fill DP table with optimal values
    fill_dp_table(tiles, dp)
    
    # Step 4: Extract and return the final answer
    return extract_result(dp)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("STRATEGIC TILE SHATTER - MODULAR FUNCTIONAL APPROACH")
    print("=" * 70)
    
    # Test Case 1: Standard configuration
    print("\nTest Case 1: Standard Tile Configuration")
    print("-" * 70)
    
    input_1 = [3, 1, 5, 8]
    output_1 = max_shatter_points(input_1)
    expected_output_1 = 167
    
    print(f"Input Multipliers: {input_1}")
    print(f"Output (Calculated): {output_1}")
    print(f"Output (Expected):   {expected_output_1}")
    
    verification_1 = "PASS" if output_1 == expected_output_1 else "FAIL"
    print(f"Status: {verification_1}")
    
    # Test Case 2: Minimal configuration
    print("\nTest Case 2: Minimal Tile Configuration")
    print("-" * 70)
    
    input_2 = [1, 5]
    output_2 = max_shatter_points(input_2)
    expected_output_2 = 10
    
    print(f"Input Multipliers: {input_2}")
    print(f"Output (Calculated): {output_2}")
    print(f"Output (Expected):   {expected_output_2}")
    
    verification_2 = "PASS" if output_2 == expected_output_2 else "FAIL"
    print(f"Status: {verification_2}")
    
    print("\n" + "=" * 70)
    if verification_1 == "PASS" and verification_2 == "PASS":
        print("SUCCESS: All validation tests passed!")
    else:
        print("FAILURE: One or more tests did not pass")
    print("=" * 70 + "\n")
