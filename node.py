from copy import deepcopy
import numpy as np
from math import inf
import itertools

class Node:

    tab_stat = []
    deadlock_map = []

    def __init__(self, sokoPuzzle, parent=None, move="", c=1):
        self.state = sokoPuzzle
        self.parent = parent
        self.c = c  # step cost, always 1 in this case
        
        if self.parent is None:
            self.g = 0  # initial node has no path cost
            self.moves = move
        else:
            self.g = self.parent.g + self.c  # accumulate path cost
            self.moves = self.parent.moves + move
        
        self.f = self.g  # initial fitness function value

    def getSolution(self):
        node = self
        solution = []
        while node:
            height = len(node.state.tab_dyn)
            width = len(node.state.tab_dyn[0])
            state = deepcopy(Node.tab_stat)
            for i, j in itertools.product(range(height), range(width)):
                if node.state.tab_dyn[i][j] == 'R':
                    state[i][j] = 'R' if state[i][j] == ' ' else '.'
                elif node.state.tab_dyn[i][j] == 'B':
                    state[i][j] = 'B' if state[i][j] == ' ' else '*'
            solution.append(state)
            node = node.parent
        return solution[::-1]

    def costHeur(self, heuristic=1):  # Calculate heuristic cost
        # Available heuristics are stored in a dictionary
        heuristics = {
            1: self.heuristic1(),
            2: self.heuristic2(),
            3: self.heuristic3()
        }
        return heuristics[heuristic]

    def setF(self, heuristic=1):  # Set the f value for the current node
        h = self.costHeur(heuristic)  # Calculate heuristic value
        self.f = self.g + h  # f = g + h
        return self.f  # Return f for sorting

    def getPath(self):
        path = []
        node = self
        while node is not None:
            path.append(node)
            node = node.parent
        return path[::-1]

    def heuristic1(self):
        tab_stat = np.array(Node.tab_stat)
        S_indices_x, S_indices_y = np.where(tab_stat == 'S')
        left_storage = len(S_indices_x)
        for ind_x, ind_y in zip(S_indices_x, S_indices_y):
            if self.state.tab_dyn[ind_x][ind_y] == 'B':
                left_storage -= 1
        return left_storage

    def heuristic2(self):
        tab_stat = np.array(Node.tab_stat)
        S_indices_x, S_indices_y = np.where(tab_stat == 'S')
        tab_dyn = np.array(self.state.tab_dyn)
        B_indices_x, B_indices_y = np.where(tab_dyn == 'B')
        sum_distance = 0
        storage_left = len(S_indices_x)
        for b_ind_x, b_ind_y in zip(B_indices_x, B_indices_y):
            min_distance = inf
            for s_ind_x, s_ind_y in zip(S_indices_x, S_indices_y):
                distance = abs(b_ind_x - s_ind_x) + abs(b_ind_y - s_ind_y)
                if distance == 0:
                    storage_left -= 1
                if distance < min_distance:
                    min_distance = distance
            sum_distance += min_distance
        return sum_distance + 2 * storage_left

    def heuristic3(self):
        tab_stat = np.array(Node.tab_stat)
        S_indices_x, S_indices_y = np.where(tab_stat == 'S')
        tab_dyn = np.array(self.state.tab_dyn)
        B_indices_x, B_indices_y = np.where(tab_dyn == 'B')
        sum_distance = 0
        storage_left = len(S_indices_x)
        min_distance_br = inf
        for b_ind_x, b_ind_y in zip(B_indices_x, B_indices_y):
            distance_br = abs(b_ind_x - self.state.robot_position[0]) + abs(b_ind_y - self.state.robot_position[1])
            if distance_br < min_distance_br:
                min_distance_br = distance_br
            min_distance = inf
            for s_ind_x, s_ind_y in zip(S_indices_x, S_indices_y):
                distance = abs(b_ind_x - s_ind_x) + abs(b_ind_y - s_ind_y)
                if distance == 0:
                    storage_left -= 1
                if distance < min_distance:
                    min_distance = distance
            sum_distance += min_distance
        return sum_distance + min_distance_br + 2 * storage_left

