import unittest
from logic import Board, Ape, Color

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_board(self):
        self.assertEqual(len(self.board.grid), 8)
        self.assertTrue(all(len(row) == 8 for row in self.board.grid))
        self.assertTrue(all(cell == ' ' for row in self.board.grid for cell in row))

    def test_display(self):
        try:
            self.board.display()
        except Exception:
            self.fail("Display method raised an exception")

class TestPiece(unittest.TestCase):
    def test_Ape_initialization(self):
        Ape_piece = Ape('red', (0, 0))
        self.assertEqual(Ape_piece.get_color(), 'red')
        self.assertEqual(Ape_piece.get_position(), (0, 0))

    def test_Ape_move(self):
        Ape_piece = Ape('blue', (0, 0))
        Ape_piece.move((1, 1))
        self.assertEqual(Ape_piece.get_position(), (1, 1))

    def test_Ape_string_representation(self):
        red_Ape = Ape('red', (0, 0))
        blue_Ape = Ape('blue', (0, 0))
        self.assertIn('A', str(red_Ape)) 
        self.assertIn('A', str(blue_Ape))

if __name__ == '__main__':
    unittest.main()
