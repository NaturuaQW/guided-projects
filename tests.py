import unittest
from main import Maze
from main import Window



class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 10
        num_rows = 10
        win = Window(600, 800)
        m1 = Maze(0, 0, num_cols, num_rows, 10, 10, win)
        self.assertEqual(
            len(m1.cells),
            num_cols * num_rows,
        )


if __name__ == "__main__":
    unittest.main()

