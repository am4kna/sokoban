from collections import deque  
from tkinter import *  
from node import *  

class Search:

    @staticmethod
    def breadthFirst(initial_node, window, deadlock_detection=False):
        # Check if the start node is already the goal
        if initial_node.state.isGoal(Node.tab_stat):
            return initial_node.getPath(), 0  # Return path and step count
        elif deadlock_detection:
            # If deadlock detection is enabled, check for deadlock at the initial node
            if initial_node.state.isDeadLock(Node.deadlock_map):
                return None, -1  # Return failure if deadlock is detected

        # Initialize the OPEN queue (FIFO) and CLOSED list
        open = deque([initial_node])  # OPEN is a deque to hold nodes to explore
        closed = list()  # CLOSED is a list to hold explored nodes
       
        step = 0  # Step counter to track the number of iterations
        while True:
            step += 1  # Increment step count
            
            # Delete the last label from the window if it exists
            try:
                label12.destroy()
            except:
                pass

            # Display the current step in the window
            label12 = Label(window, text=f'*** Step {step} ***', bg='#c45242', fg='white')
            label12.pack()
            window.update()  # Update GUI with new step label

            # Check if the OPEN queue is empty, indicating goal was not found
            if len(open) == 0:
                return None, -1  # Return failure if goal not found
            
            # Get and remove the first element from the OPEN queue
            current = open.popleft()
            
            # Add the current node to the CLOSED list to mark as explored
            closed.append(current)
            
            if deadlock_detection:
                # Skip node if it's in a deadlock state
                if current.state.isDeadLock(Node.deadlock_map):
                    continue
                        
            # Generate successors of the current node
            successors = current.state.successorFunction(current)
            while len(successors) != 0:
                child, action = successors.popleft()  # Get a successor and the action taken

                # Check if the child's state is not in OPEN or CLOSED lists
                if (child.state.tab_dyn not in [n.state.tab_dyn for n in closed] and \
                    child.state.tab_dyn not in [n.state.tab_dyn for n in open]): 

                    # Add the child node to the OPEN queue
                    open.append(child)

                    # Check if the child node is the goal
                    if child.state.isGoal(Node.tab_stat):
                        label12.destroy()  # Remove last step label from GUI
                        return child.getPath(), step  # Return solution path and step count

    @staticmethod
    def Astar(init_node, window, heuristic=1, deadlock_detection=False):
        # Check if the initial node is the goal
        if init_node.state.isGoal(Node.tab_stat):
            return init_node.getPath(), 0  # Return path if already at goal
        elif deadlock_detection and init_node.state.isDeadLock(Node.deadlock_map):
            return None, -1  # Return failure if initial state is a deadlock

        # Set initial path cost and fitness value (f) based on the chosen heuristic
        init_node.g = 0 
        init_node.setF(heuristic)  # Calculate initial f value with heuristic

        # Initialize the OPEN list as a priority queue and CLOSED set
        open = deque([init_node])  # OPEN deque used as a priority queue
        closed = set()  # CLOSED is a set of tuples representing explored states
        step = 0  # Step counter

        while open:
            step += 1  # Increment step count

            # Display the current step in the window (for GUI)
            try:
                label123.destroy()
            except:
                pass

            # Create a label for the current step and update the GUI
            label123 = Label(window, text=f'*** Step {step} ***', bg='#c45242', fg='white')
            label123.pack()
            window.update()

            # Sort OPEN by f-value to prioritize nodes with the lowest f (A* behavior)
            open = deque(sorted(open, key=lambda node: node.setF(heuristic)))

            # Pop the node with the lowest f-value from OPEN
            current = open.popleft()

            # Check if the current node is the goal
            if current.state.isGoal(Node.tab_stat):
                label123.destroy()  # Remove step label from GUI
                return current.getPath(), step  # Return solution path and step count

            # Add current node's state as a unique tuple to CLOSED
            closed.add(tuple(map(tuple, current.state.tab_dyn)))  # Convert 2D list to tuple of tuples

            # Generate successors of the current node
            successors = current.state.successorFunction(current)
            while successors:
                child, action = successors.popleft()  # Get a successor and the action taken
                child.g = current.g + 1  # Increment path cost for the child
                
                child.setF(heuristic)  # Set f-value for the child node

                # Skip child if it's a deadlock state
                if deadlock_detection and child.state.isDeadLock(Node.deadlock_map):
                    continue

                # Convert child's state to a tuple for easy comparison
                child_state_tuple = tuple(map(tuple, child.state.tab_dyn))
                
                # Skip child if it has already been explored (exists in CLOSED)
                if child_state_tuple in closed:
                    continue

                # Check if the child is already in OPEN with a better f-value
                open_states = [tuple(map(tuple, node.state.tab_dyn)) for node in open]
                if child_state_tuple in open_states:
                    index = open_states.index(child_state_tuple)  # Find index in OPEN
                    # Replace child in OPEN if it has a better f-value
                    if child.setF(heuristic) < open[index].setF(heuristic):
                        open[index] = child
                else:
                    open.append(child)  # Add new child to OPEN if not already there

        # If OPEN is empty and goal not found, return failure
        return None, -1
