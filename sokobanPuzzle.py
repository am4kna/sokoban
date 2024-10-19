import numpy as np

""" Representations:
O => Obstacle
S => Storage
B => Block
R => Robot
* => Block on a storage
. => Robot on a storage """


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
            return self.move(self.moves[action], tab_stat)
        return False

    def move(self, direction, tab_stat):
        """General method to move the robot in the given direction."""
        dx, dy = direction
        robot_x, robot_y = self.robot_position
        new_robot_x, new_robot_y = robot_x + dx, robot_y + dy
        
        # Check boundaries and wall
        if not self.is_in_bounds(new_robot_x, new_robot_y) or tab_stat[new_robot_x][new_robot_y] == 'O':
            return False

        # Check if the robot is moving towards a box
        if self.tab_dyn[new_robot_x][new_robot_y] == 'B':
            # Check if the box can be pushed
            new_box_x, new_box_y = new_robot_x + dx, new_robot_y + dy
            if not self.is_in_bounds(new_box_x, new_box_y) or self.tab_dyn[new_box_x][new_box_y] == 'B' or tab_stat[new_box_x][new_box_y] == 'O':
                return False  # Can't push the box

            # Move the box
            self.update_position((new_box_x, new_box_y), (new_robot_x, new_robot_y), 'B', tab_stat)

        # Move the robot
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