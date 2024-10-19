from copy import deepcopy

class Node:
    def __init__(self, sokobanPuzzle, parent=None, action="", g=1, tab_stat=None):
        self.state = sokobanPuzzle  # SokobanPuzzle state
        self.parent = parent
        self.action = action  # Action that led to this state
        self.g = g if parent is None else parent.g + g  # Path cost (step cost = 1)
        self.depth = 0 if parent is None else parent.depth + 1
        self.moves = "" if parent is None else parent.moves + action
        self.tab_stat = tab_stat  # Passing static elements as an instance variable

    def successorFunction(self):
        """Generates pairs of (action, successor) representing all valid moves."""
        successors = []
        for action, direction in self.state.moves.items():  # Iterate over the moves dictionary
            next_state = deepcopy(self.state)  # Create a deep copy of the current puzzle state
            if next_state.executeMove(action, self.tab_stat):  # Check if the move is valid
                # Create the successor node
                successor_node = Node(next_state, self, action, tab_stat=self.tab_stat)
                print(f"Action: {action}, Generated successor with depth {successor_node.depth}")
                # Append the tuple (action, successor_node) to the list
                successors.append((action, successor_node))
        print(f"Total successors generated: {len(successors)}")
        return successors

    def setF(self, heuristic=1):
        """Sets the f value based on the chosen heuristic."""
        self.f = self.g + self.heuristic(heuristic)
        print(f"Setting f-value for node. g = {self.g}, heuristic = {self.f - self.g}, f = {self.f}")

    def heuristic(self, choice=1):
        """Different heuristic choices."""
        if choice == 1:
            return self.heuristic1()  # Example heuristic
        elif choice == 2:
            return self.heuristic2()
        else:
            return self.heuristic3()

    def heuristic1(self):
        # Example heuristic (this can be customized further)
        print("Calculating heuristic1...")
        return 0  # Placeholder for a heuristic

    def heuristic2(self):
        # Another example heuristic
        print("Calculating heuristic2...")
        return 0  # Placeholder for a heuristic

    def heuristic3(self):
        # Another example heuristic
        print("Calculating heuristic3...")
        return 0  # Placeholder for a heuristic
