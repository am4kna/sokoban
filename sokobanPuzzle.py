from copy import deepcopy
import numpy as np

from node import Node

class SokobanPuzzle:

    def __init__(self, tab_dyn, robot_position):
        self.tab_dyn = tab_dyn  # Dynamic elements of the puzzle (robot, boxes)
        self.robot_position = robot_position  # Robot's position tuple
        self.moves = {
            "U": (-1, 0),  # Move Up: Decrease row
            "D": (1, 0),   # Move Down: Increase row
            "L": (0, -1),  # Move Left: Decrease column
            "R": (0, 1)    # Move Right: Increase column
        }

    def isGoal(self, tab_stat):
        # Check if all targets ('S') have boxes ('B' or '*')
        S_indices_x, S_indices_y = np.where(np.array(tab_stat) == 'S')  # Get all target spaces
        for ind_x, ind_y in zip(S_indices_x, S_indices_y):
            if self.tab_dyn[ind_x][ind_y] != 'B':  # Target space must have a box
                return False
        return True
    
    def executeMove(self, action, tab_stat):
        """Executes a move in the given direction."""
        if action in self.moves:
            print(f"Executing move: {action}")
            success = self.move(self.moves[action], tab_stat)
            print(f"Move result: {'Success' if success else 'Failed'}")
            self.print_board()  # Output the board state after the move
            return success
        return False

    def move(self, direction, tab_stat):
        """General method to move the robot in the given direction."""
        dx, dy = direction
        robot_x, robot_y = self.robot_position
        new_robot_x, new_robot_y = robot_x + dx, robot_y + dy
        
        # Check boundaries and wall
        if not self.is_in_bounds(new_robot_x, new_robot_y) or tab_stat[new_robot_x][new_robot_y] == 'O':
            print("Blocked by boundary or wall.")
            return False

        # Check if the robot is moving towards a box
        if self.tab_dyn[new_robot_x][new_robot_y] == 'B':
            # Check if the box can be pushed
            new_box_x, new_box_y = new_robot_x + dx, new_robot_y + dy
            if not self.is_in_bounds(new_box_x, new_box_y) or self.tab_dyn[new_box_x][new_box_y] == 'B' or tab_stat[new_box_x][new_box_y] == 'O':
                print("Cannot push the box.")
                return False  # Can't push the box

            # Move the box
            print(f"Pushing box from ({new_robot_x}, {new_robot_y}) to ({new_box_x}, {new_box_y})")
            self.update_position((new_box_x, new_box_y), (new_robot_x, new_robot_y), 'B', tab_stat)

        # Move the robot
        print(f"Moving robot from ({robot_x}, {robot_y}) to ({new_robot_x}, {new_robot_y})")
        self.update_position((new_robot_x, new_robot_y), (robot_x, robot_y), 'R', tab_stat)
        self.robot_position = (new_robot_x, new_robot_y)
        return True

    def is_in_bounds(self, x, y):
        """Check if the position is within the bounds of the grid."""
        return 0 <= x < len(self.tab_dyn) and 0 <= y < len(self.tab_dyn[0])

    def update_position(self, new_pos, old_pos, element, tab_stat):
        """Update the position of the robot or box."""
        new_x, new_y = new_pos
        old_x, old_y = old_pos

        # Update the new position (check if it's a target space or not)
        if tab_stat[new_x][new_y] == 'S':
            self.tab_dyn[new_x][new_y] = '*' if element == 'B' else '.'
        else:
            self.tab_dyn[new_x][new_y] = element

        # Update the old position
        if tab_stat[old_x][old_y] == 'S':
            self.tab_dyn[old_x][old_y] = 'S'
        else:
            self.tab_dyn[old_x][old_y] = ' '

    def print_board(self):
        """Print the current dynamic state of the board."""
        for row in self.tab_dyn:
            print(''.join(row))
        print("\n")

    def succ(self, tab_stat):
        """Generates pairs of (action, successor) representing all valid moves."""
        successors = []
        for action, direction in self.moves.items():  # Iterate over the moves dictionary
            next_state = deepcopy(self)  # Create a deep copy of the current puzzle state
            if next_state.executeMove(action, tab_stat):  # Check if the move is valid
                # Create the successor node
                successor_node = Node(next_state, action=action, tab_stat=tab_stat)
                print(f"Action: {action}, Generated successor with depth {successor_node.depth}")
                # Append the tuple (action, successor_node) to the list
                successors.append((action, successor_node))
        print(f"Total successors generated: {len(successors)}")
        return successors
