from sokobanPuzzle import SokobanPuzzle
from node import Node

# Define a small Sokoban board (static elements)
tab_stat = [
    ['O', 'O', 'O', 'O', 'O'],
    ['O', 'S', ' ', ' ', 'O'],
    ['O', ' ', ' ', 'B', 'O'],
    ['O', ' ', ' ', ' ', 'S'],
    ['O', 'O', 'O', 'O', 'O']
]

# Define the dynamic elements (robot and boxes)
tab_dyn = [
    ['O', 'O', 'O', 'O', 'O'],
    ['O', 'S', ' ', ' ', 'O'],
    ['O', ' ', 'R', 'B', 'O'],
    ['O', ' ', ' ', ' ', 'S'],
    ['O', 'O', 'O', 'O', 'O']
]

# Define the robot's initial position
robot_position = (2, 2)

# Initialize Sokoban puzzle
puzzle = SokobanPuzzle(tab_dyn, robot_position)

# Create a Node representing the initial state
initial_node = Node(puzzle, tab_stat=tab_stat)

# Call the successor function to generate moves
successors = initial_node.successorFunction()

# Print out the actions and the resulting states
for action, successor in successors:
    print(f"Action: {action}")
    successor.state.print_board()  # Print the board after each move
