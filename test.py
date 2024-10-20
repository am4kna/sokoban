import unittest
from sokobanPuzzle import SokobanPuzzle

from node import Node

class TestSokobanGame(unittest.TestCase):
    def setUp(self):
        # Initialize a simple Sokoban puzzle for testing
        self.tab_stat = [
            ['O', 'O', 'O', 'O', 'O'],
            ['O', ' ', ' ', 'S', 'O'],
            ['O', ' ', 'B', ' ', 'O'],
            ['O', 'R', ' ', ' ', 'O'],
            ['O', 'O', 'O', 'O', 'O']
        ]  # Static elements: O = Wall, S = Goal

        self.tab_dyn = [
            ['O', 'O', 'O', 'O', 'O'],
            ['O', ' ', ' ', 'S', 'O'],
            ['O', ' ', 'B', ' ', 'O'],
            ['O', 'R', ' ', ' ', 'O'],
            ['O', 'O', 'O', 'O', 'O']
        ]  # Dynamic elements: R = Robot, B = Box

        self.robot_position = (3, 1)
        self.puzzle = SokobanPuzzle(self.tab_dyn, self.robot_position)

        # Set Node static variable tab_stat
        Node.tab_stat = self.tab_stat

    def test_initial_state(self):
        # Test the initial robot position
        self.assertEqual(self.puzzle.robot_position, (3, 1))

        # Test the initial dynamic state
        self.assertEqual(self.puzzle.tab_dyn[3][1], 'R')  # Robot at position (3, 1)
        self.assertEqual(self.puzzle.tab_dyn[2][2], 'B')  # Box at position (2, 2)



    def test_move_box(self):
        # Move the robot up to push the box
        self.puzzle.executeMove('U', self.tab_stat)
        self.puzzle.executeMove('R', self.tab_stat)
        self.puzzle.executeMove('R', self.tab_stat)  
        self.puzzle.executeMove('D', self.tab_stat)  
        self.puzzle.executeMove('R', self.tab_stat)  
        self.puzzle.executeMove('U', self.tab_stat)  








if __name__ == "__main__":
    unittest.main()
