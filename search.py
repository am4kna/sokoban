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
        elif deadlock_detection:
            if init_node.state.isDeadLock(Node.deadlock_map):
                return None, -1
        
        init_node.setF(heuristic)
        # Create the OPEN priority queue and the CLOSED list
        open = deque([init_node])
        closed = list()
        step = 0
        while True:
            step += 1
            
            # Delete the last label if it exists
            try:
                label123.destroy()
            except:
                pass
            
            label123 = Label(window, text=f'*** Step {step} ***', bg='#c45242', fg='white')
            label123.pack()
            window.update()
            
            # Check if the OPEN queue is empty => goal not found
            if len(open) == 0:
                return None, -1
            
            # Sort the open list by the f value
            open = deque(sorted(list(open), key=lambda node: node.f))

            # Get the first element of the OPEN queue
            current = open.popleft()

            # Put the current node in the CLOSED list
            closed.append(current)

            # Check if the current node is the goal
            if current.state.isGoal(Node.tab_stat):
                label123.destroy()
                return current.getPath(), step
            elif deadlock_detection:
                if current.state.isDeadLock(Node.deadlock_map):
                    continue
            
            # Generate the successors of the current node
            successors = current.state.successorFunction(current)
            while len(successors) != 0:
                child, move = successors.popleft()
                child.setF(heuristic)

                # Check if the child is in the OPEN queue
                if child.state.tab_dyn in [node.state.tab_dyn for node in open]:
                    index = [node.state.tab_dyn for node in open].index(child.state.tab_dyn)
                    if child.f < open[index].f:
                        open[index] = child
                # Check if the child is not in CLOSED list
                elif child.state.tab_dyn not in [node.state.tab_dyn for node in closed]:
                    open.append(child)
                # If the child is in CLOSED list
                else:
                    index = [node.state.tab_dyn for node in closed].index(child.state.tab_dyn)
                    if child.f < closed[index].f:
                        closed.remove(closed[index])
                        open.append(child)
