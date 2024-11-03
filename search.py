from collections import deque
from tkinter import *
from node import *

class Search:

    @staticmethod
    def breadthFirst(initial_node, window, deadlock_detection=False):
        # Check if the start element is the goal
        if initial_node.state.isGoal(Node.tab_stat):
            return initial_node.getPath(), 0
        elif deadlock_detection:
            if initial_node.state.isDeadLock(Node.deadlock_map):
                return None, -1

        # Create the OPEN FIFO queue and the CLOSED list
        open = deque([initial_node])
        closed = list()
       
        step = 0
        while True:
            step += 1
            
            # Delete the last label if it exists
            try:
                label12.destroy()
            except:
                pass

            label12 = Label(window, text=f'*** Step {step} ***', bg='#c45242', fg='white')
            label12.pack()
            window.update()

            # Check if the OPEN queue is empty => goal not found
            if len(open) == 0:
                return None, -1
            
            # Get the first element of the OPEN queue
            current = open.popleft()
            
            # Put the current node in the CLOSED list
            closed.append(current)
            
            if deadlock_detection:
                if current.state.isDeadLock(Node.deadlock_map):
                    continue
                        
            # Generate the successors of the current node
            successors = current.state.successorFunction(current)
            while len(successors) != 0:
                child, move = successors.popleft()

                # Check if the child is not in the OPEN queue and the CLOSED list
                if (child.state.tab_dyn not in [n.state.tab_dyn for n in closed] and \
                    child.state.tab_dyn not in [n.state.tab_dyn for n in open]): 

                    # Put the child in the OPEN queue 
                    open.append(child)

                    # Check if the child is the goal
                    if child.state.isGoal(Node.tab_stat):
                        label12.destroy()
                        return child.getPath(), step

    @staticmethod
    def Astar(init_node, window, heuristic=1, deadlock_detection=False):
        # Check if the start element is the goal
        if init_node.state.isGoal(Node.tab_stat):
            return init_node.getPath(), 0
        elif deadlock_detection and init_node.state.isDeadLock(Node.deadlock_map):
            return None, -1

        # Set initial setF(heuristic) value based on the chosen heuristic
        init_node.costHeur(heuristic)

        # Initialize the OPEN list as a priority queue and the CLOSED set
        open = deque([init_node])
        closed = set()  # CLOSED is a set of tuples representing states
        step = 0

        while open:
            step += 1

            # Display the current step in the window (if GUI is used)
            try:
                label123.destroy()
            except:
                pass

            label123 = Label(window, text=f'*** Step {step} ***', bg='#c45242', fg='white')
            label123.pack()
            window.update()

            # Sort OPEN by setF(heuristic) value to prioritize nodes with the lowest setF(heuristic) (A* behavior)
            open = deque(sorted(open, key=lambda node: node.setF(heuristic)))

            # Pop the node with the lowest setF(heuristic) value from OPEN
            current = open.popleft()

            # Check if the current node is the goal
            if current.state.isGoal(Node.tab_stat):
                label123.destroy()
                return current.getPath(), step

            # Add current node's unique state as a tuple to CLOSED
            closed.add(tuple(map(tuple, current.state.tab_dyn)))  # Convert 2D list to a tuple of tuples

            # Generate successors of the current node
            successors = current.state.successorFunction(current)
            while successors:
                child, move = successors.popleft()
                child.costHeur(heuristic)

                # Skip child if it's a deadlock state
                if deadlock_detection and child.state.isDeadLock(Node.deadlock_map):
                    continue

                # Check if the child’s state (converted to a tuple) is already in CLOSED
                child_state_tuple = tuple(map(tuple, child.state.tab_dyn))
                if child_state_tuple in closed:
                    continue

                # Check if child is already in OPEN and update if found with a better setF(heuristic) value
                open_states = [tuple(map(tuple, node.state.tab_dyn)) for node in open]
                if child_state_tuple in open_states:
                    index = open_states.index(child_state_tuple)
                    if child.setF(heuristic) < open[index].setF(heuristic):
                        open[index] = child  # Replace with better path
                else:
                    open.append(child)  # Add new child to OPEN if not already there

        # If OPEN is empty and goal not found
        return None, -1
