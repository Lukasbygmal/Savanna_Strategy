import unittest
from logic import Board, Ape, Snake, Crab, Meerkat, Lynx

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_board_empty(self):
        for row in self.board.grid:
            for cell in row:
                self.assertEqual(cell, None)

    def test_pos_is_empty(self):
        position = (3, 3)
        self.assertTrue(self.board.pos_is_empty(position))
        
    def test_place_piece(self):
        ape = Ape("red", (3, 3))
        self.board.place_piece(ape, (3, 3))
        self.assertEqual(self.board.get_piece_at_pos((3, 3)), ape)
        self.assertFalse(self.board.pos_is_empty((3, 3)))

    def test_pos_inside_board(self):
        self.assertTrue(self.board.pos_inside_board((0, 0)))
        self.assertTrue(self.board.pos_inside_board((7, 7)))
        self.assertFalse(self.board.pos_inside_board((8, 8)))
        self.assertFalse(self.board.pos_inside_board((-1, 0)))

class TestApe(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.ape = Ape("red", (3, 3))
        self.board.place_piece(self.ape, (3, 3))

    def test_ape_possible_moves(self):
        moves = self.ape.get_possible_moves(self.ape.get_position(), self.board)
        expected_moves = [(4, 3), (5, 3)]
        self.assertEqual(sorted(moves), sorted(expected_moves))

class TestSnake(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.snake = Snake("blue", (4, 4))
        self.board.place_piece(self.snake, (4, 4))

    def test_snake_possible_moves(self):
        moves = self.snake.get_possible_moves(self.snake.get_position(), self.board)
        expected_moves = [(5, 5), (3, 3), (3, 5), (5, 3), (6, 4), (2, 4), (4, 6), (4, 2), 
                          (7, 5), (7, 3), (1, 5), (1, 3), (5, 7), (3, 7), (5, 1), (3, 1),
                          (4, 0), (0, 4)]
        self.assertEqual(sorted(moves), sorted(expected_moves))

class TestCrab(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.crab = Crab("red", (4, 4))
        self.board.place_piece(self.crab, (4, 4))

    def test_crab_possible_moves(self):
        moves = self.crab.get_possible_moves(self.crab.get_position(), self.board)
        expected_moves = [(3, 4), (5, 4), (4,3), (4,2), (4,1), (4,0), (4,5), (4,6), (4,7)]
        self.assertEqual(sorted(moves), sorted(expected_moves))

class TestMeerkat(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.meerkat = Meerkat("blue", (3, 3))
        self.board.place_piece(self.meerkat, (3, 3))

    def test_meerkat_possible_moves(self):
        moves = self.meerkat.get_possible_moves(self.meerkat.get_position(), self.board)
        expected_moves = [(4, 3), (5, 3), (2, 3), (1, 3), (3, 4), (3, 5), (3, 2), (3, 1)]
        self.assertEqual(sorted(moves), sorted(expected_moves))

class TestLynx(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.lynx = Lynx("red", (3, 3))
        self.board.place_piece(self.lynx, (3, 3))

    def test_lynx_possible_moves(self):
        moves = self.lynx.get_possible_moves(self.lynx.get_position(), self.board)
        expected_moves = [
            (4, 3), (2, 3), (3, 4), (3, 2), (4, 4), (5, 5), (6, 6), (7, 7),
            (2, 2), (1, 1), (0, 0), (2, 4), (1, 5), (0, 6), (4, 2), (5, 1),
            (6, 0),               
        ]
        self.assertEqual(sorted(moves), sorted(expected_moves))


if __name__ == "__main__":
    unittest.main()
