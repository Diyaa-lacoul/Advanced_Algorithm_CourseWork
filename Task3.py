"""
Minimum Service Centers - Object-Oriented Greedy DFS

Provides a ServiceCenterPlanner class that encapsulates the greedy DFS logic.
This version structures code for clarity and testability.
"""

from typing import Optional, List


class TreeNode:
    """Simple binary tree node class used for the planner."""
    def __init__(self, val: int = 0, left: 'Optional[TreeNode]' = None, right: 'Optional[TreeNode]' = None):
        self.val = val
        self.left = left
        self.right = right


class ServiceCenterPlanner:
    """
    Planner that determines the minimum number of service centers using
    a post-order greedy DFS with three states per node.

    States:
        0 -> NOT COVERED
        1 -> HAS CENTER
        2 -> COVERED (no center)
    """

    NOT_COVERED = 0
    HAS_CENTER = 1
    COVERED = 2

    def __init__(self):
        self.service_centers_count = 0

    def _dfs_state(self, node: Optional[TreeNode]) -> int:
        """
        Post-order traversal returning the state of `node`.

        Logic:
        - If either child is NOT_COVERED -> place center here (HAS_CENTER)
        - Else if either child HAS_CENTER -> this node is COVERED
        - Else -> this node is NOT_COVERED
        """
        if node is None:
            return ServiceCenterPlanner.COVERED

        left_child_state = self._dfs_state(node.left)
        right_child_state = self._dfs_state(node.right)

        # If a child is not covered, we must put a center here
        if left_child_state == ServiceCenterPlanner.NOT_COVERED or right_child_state == ServiceCenterPlanner.NOT_COVERED:
            self.service_centers_count += 1
            return ServiceCenterPlanner.HAS_CENTER

        # If any child has a center, current node is covered
        if left_child_state == ServiceCenterPlanner.HAS_CENTER or right_child_state == ServiceCenterPlanner.HAS_CENTER:
            return ServiceCenterPlanner.COVERED

        # Otherwise node is not yet covered
        return ServiceCenterPlanner.NOT_COVERED

    def min_centers(self, root: Optional[TreeNode]) -> int:
        """
        Compute and return minimum number of centers for the tree rooted at `root`.
        Ensures the root is covered (extra center added if needed).
        """
        self.service_centers_count = 0
        root_state = self._dfs_state(root)
        if root_state == ServiceCenterPlanner.NOT_COVERED:
            self.service_centers_count += 1
        return self.service_centers_count


def build_tree_from_level(values: List[Optional[int]]) -> Optional[TreeNode]:
    """
    Helper to build tree from level-order list. None represents missing node.
    """
    if not values:
        return None
    nodes = [TreeNode(v) if v is not None else None for v in values]
    kids = nodes[::-1]
    root = kids.pop()
    for node in nodes:
        if node:
            if kids:
                node.left = kids.pop()
            if kids:
                node.right = kids.pop()
    return root


if __name__ == "__main__":
    # Given example: {0, 0, null, 0, null, 0, null, null, 0}
    level_order = [0, 0, None, 0, None, 0, None, None, 0]
    root_node = build_tree_from_level(level_order)

    planner = ServiceCenterPlanner()
    result = planner.min_centers(root_node)
    print("OOP Planner Result:", result)
    print("Expected: 2")
