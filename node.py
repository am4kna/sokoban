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

    def getPath(self):
        """Returns a list of states representing the path from the initial state to the current node."""
        path = []
        node = self
        while node is not None:
            path.append(node.state.tab_dyn)
            node = node.parent
        return path[::-1]  # Return the path from initial state to goal

    def getSolution(self):
        """Returns a list of actions taken to reach the current node."""
        solution = []
        node = self
        while node.parent is not None:
            solution.append(node.action)
            node = node.parent
        return solution[::-1]  # Return the list of actions from initial state to goal

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
        print("Calculating heuristic1...")
        return 0  # Placeholder for a heuristic

    def heuristic2(self):
        print("Calculating heuristic2...")
        return 0  # Placeholder for a heuristic

    def heuristic3(self):
        print("Calculating heuristic3...")
        return 0  # Placeholder for a heuristic
