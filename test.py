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
print("Initializing Sokoban Puzzle with the following dynamic board state:")
puzzle = SokobanPuzzle(tab_dyn, robot_position)
puzzle.print_board()

# Create a Node representing the initial state
print("Creating initial Node for the puzzle.")
initial_node = Node(puzzle, tab_stat=tab_stat)

# Call the successor function from SokobanPuzzle to generate moves
print("\nGenerating successors (possible moves) from the initial state...")
successors = puzzle.successorFunction(tab_stat)

# Print out the actions and the resulting states
if successors:
    print("\nSuccessors generated. Printing actions and resulting states:")
else:
    print("No successors generated!")

for idx, (action, successor) in enumerate(successors):
    print(f"\nSuccessor {idx + 1}: Action -> {action}")
    print("Resulting state of the board after this move:")
    successor.state.print_board()  # Print the board after each move
    print(f"Actions taken so far: {successor.moves}")
