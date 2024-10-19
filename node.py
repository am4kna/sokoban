from copy import deepcopy

class Node:
    def __init__(self, state, parent=None, action="", g=1, tab_stat=None):
        self.state = state  # SokobanPuzzle state
        self.parent = parent
        self.action = action  # Action that led to this state
        self.g = g if parent is None else parent.g + g  # Path cost (step cost = 1)
        self.depth = 0 if parent is None else parent.depth + 1
        self.moves = "" if parent is None else parent.moves + action
        self.tab_stat = tab_stat  # Passing static elements as an instance variable

    def successorFunction(self):  
        successors = []
        for move in self.state.moves:
            next_state = deepcopy(self.state)
            if next_state.executeMove(move, self.tab_stat):  # Valid move check
                successors.append((move, Node(next_state, self, move, tab_stat=self.tab_stat)))
        return successors

    def getPath(self):  # Retrieve the sequence of states from start to goal
        path = []
        node = self
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]  # Reverse to get the correct order from start to goal

    def getSolution(self):  # Retrieve the sequence of moves (actions)
        solution = []
        node = self
        while node.parent:
            solution.append(node.action)
            node = node.parent
        return solution[::-1]  # Reverse the solution

    def setF(self, heuristic=1):  # Calculates f = g + h
        self.f = self.g + self.heuristic(heuristic)

    def heuristic(self, choice=1):
        """Different heuristic choices."""
        if choice == 1:
            return self.heuristic1()  # Example heuristic
        elif choice == 2:
            return self.heuristic2()
        else:
            return self.heuristic3()

