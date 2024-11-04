from copy import deepcopy  
import numpy as np  
from math import inf  
import itertools

class Node:
    tab_stat = [] # the wall, space and obstacle of the puzzle are stored in a global variable to be used in the heuristic functions
    deadlock_map = []  # static variable for deadlock positions in the puzzle

    def __init__(self, sokoPuzzle, parent=None, action="", c=1):
        self.state = sokoPuzzle  
        self.parent = parent  
        if self.parent is None:  
            self.c = 0  # Initial node has no step cost
            self.g = 0  # Initial node has no path cost
            self.actions = action  # Actions taken from start to reach this node
        else:
            self.g = self.parent.g + c  # Accumulate path cost from parent
            self.actions = self.parent.actions + action  # Append current action to parent's actions

        self.f = 0  # Initialize fitness (f) value for this node

    def getSolution(self):
        node = self
        solution = []  # To store each state in the solution path
        while node:
            # Retrieve dimensions of the dynamic grid
            height = len(node.state.tab_dyn)
            width = len(node.state.tab_dyn[0])

            # Create a copy of the static grid for modification
            state = deepcopy(Node.tab_stat)
            for i, j in itertools.product(range(height), range(width)):
                # Place robot on the static grid or mark goals
                if node.state.tab_dyn[i][j] == 'R':  # Robot position
                    state[i][j] = 'R' if state[i][j] == ' ' else '.'
                elif node.state.tab_dyn[i][j] == 'B':  # Box position
                    state[i][j] = 'B' if state[i][j] == ' ' else '*'

            # Append the current modified state to the solution list
            solution.append(state)
            node = node.parent  # Move to the parent node for the previous state

        return solution[::-1]  # Return the solution path in correct order (root to current)

    def setF(self, heuristic=1):  # Calculate fitness function using heuristic cost
        # Dictionary mapping heuristic number to its respective function
        heuristics = {
            1: self.heuristic1(),
            2: self.heuristic2(),
            3: self.heuristic3()
        }
        return self.g + heuristics[heuristic]  # Return sum of path cost and heuristic cost

    def getPath(self):
        # Retrieve the path of nodes from the current node back to the root
        path = []
        node = self
        while node is not None:
            path.append(node)  # Append current node to path
            node = node.parent  # Move to parent node
        return path[::-1]  # Return path in correct order from root to current node

    def heuristic1(self):
        # Heuristic 1: Counts the number of storage locations without boxes
        tab_stat = np.array(Node.tab_stat)  # Convert static state ( the wall, space and obstacle of the puzzle ) to numpy array
        # Retrieve all the storage cells
        S_indices_x, S_indices_y = np.where(tab_stat == 'S')  # Find coordinates of storage locations
        left_storage = len(S_indices_x)  # Initialize count of storage locations

        # Check if each storage location has a box
        for ind_x, ind_y in zip(S_indices_x, S_indices_y):
            if self.state.tab_dyn[ind_x][ind_y] == 'B':  # If a box is on a storage location
                left_storage -= 1  # Decrease count of unoccupied storage locations

        return left_storage  # Return the count of storage locations without boxes

    def heuristic2(self):
        # Heuristic 2: Sum of Manhattan distances between boxes and closest storage locations
        tab_stat = np.array(Node.tab_stat)  # Convert static state to numpy array
        S_indices_x, S_indices_y = np.where(tab_stat == 'S')  # Find coordinates of storage locations
        tab_dyn = np.array(self.state.tab_dyn)  # Convert dynamic state (robot and box) to numpy array
        B_indices_x, B_indices_y = np.where(tab_dyn == 'B')  # Find coordinates of boxes

        sum_distance = 0  # Initialize sum of distances
        storage_left = len(S_indices_x)  # Count of unoccupied storage locations

        # Calculate distance for each box to the closest storage location
        for b_ind_x, b_ind_y in zip(B_indices_x, B_indices_y):
            min_distance = inf  # Start with an infinite distance
            for s_ind_x, s_ind_y in zip(S_indices_x, S_indices_y):
                distance = abs(b_ind_x - s_ind_x) + abs(b_ind_y - s_ind_y)  # Manhattan distance
                if distance == 0:
                    storage_left -= 1  # Decrease storage count if box is on a storage location
                if distance < min_distance:
                    min_distance = distance  # Update minimum distance for this box

            sum_distance += min_distance  # Add minimum distance to the sum

        return sum_distance + 2 * storage_left  # Heuristic cost with penalty for empty storage

    """ Third heuristic: Min Manhattan Distance between blocks and storage goals + Min Manhattan Distance between the robot and the blocks 
                        + 2 * Number of left storage cells"""
    def heuristic3(self):
        # Heuristic 3: Combines box-to-storage distances and robot-to-box distances
        tab_stat = np.array(Node.tab_stat)  # Convert static state to numpy array
        S_indices_x, S_indices_y = np.where(tab_stat == 'S')  # Find coordinates of storage locations
        tab_dyn = np.array(self.state.tab_dyn)  # Convert dynamic state to numpy array
        B_indices_x, B_indices_y = np.where(tab_dyn == 'B')  # Find coordinates of boxes

        sum_distance = 0  # Initialize distance sum for boxes to storage locations
        storage_left = len(S_indices_x)  # Count of unoccupied storage locations
        min_distance_br = inf  # Initialize robot-to-box minimum distance

        # For each box, calculate distances to both storage locations and robot
        for b_ind_x, b_ind_y in zip(B_indices_x, B_indices_y):
            # Distance from robot to the box
            distance_br = abs(b_ind_x - self.state.robot_position[0]) + abs(b_ind_y - self.state.robot_position[1])
            if distance_br < min_distance_br:
                min_distance_br = distance_br  # Update minimum robot-to-box distance

            min_distance = inf  # Initialize minimum box-to-storage distance
            for s_ind_x, s_ind_y in zip(S_indices_x, S_indices_y):
                distance = abs(b_ind_x - s_ind_x) + abs(b_ind_y - s_ind_y)  # Manhattan distance
                if distance == 0:
                    storage_left -= 1  # Decrease count if box is already on a storage
                if distance < min_distance:
                    min_distance = distance  # Update minimum distance for this box

            sum_distance += min_distance  # Add box-to-storage distance to the sum

        # Return combined heuristic: box-to-storage distances, robot-to-box distance, penalty for empty storage
        return sum_distance + min_distance_br + 2 * storage_left
