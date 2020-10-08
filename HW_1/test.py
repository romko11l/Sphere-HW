"""Test for TicTacToe.py"""
import unittest
from TicTacToe import TicTacGame


class TestTicTacGame(unittest.TestCase):
    def setUp(self):
        self.game1 = TicTacGame()
        self.game2 = TicTacGame(5, 5)
        self.game2._matrix[2][2] = 2
        self.game2._matrix[1][1] = 2
        self.game2._matrix[0][0] = 2
        self.game2._matrix[4][4] = 1
        # стоило сделать отдельную функцию для обращения к полю игры
        # чтобы не использовать _matrix
        # тогда можно было бы поменять логику хранения поля, меняя только её
        self.moves_list = []
        for i in range(self.game2._height):
            for j in range(self.game2._width):
                if self.game2._matrix[i][j] == 0:
                    self.moves_list.append((i, j))

    def test_init(self):
        # feeding incorrect data to the constructor
        self.assertRaises(ValueError, TicTacGame, 2, 3)
        self.assertRaises(ValueError, TicTacGame, -1, 5)
        self.assertRaises(ValueError, TicTacGame, 10, 5)

    def test_validate_move(self):
        # correct move
        calling1 = self.game1.validate_move('b2')
        self.assertEqual(calling1, (2, 'B'))
        calling2 = self.game1.validate_move('A2')
        self.assertEqual(calling2, (2, 'A'))
        # incorrect move
        self.assertRaises(ValueError, self.game1.validate_move, 'Hello')
        self.assertRaises(ValueError, self.game1.validate_move, 'a0')
        self.assertRaises(ValueError, self.game1.validate_move, 'O0')
        self.assertRaises(ValueError, self.game1.validate_move, 'aa')
        self.assertRaises(ValueError, self.game1.validate_move, '11')
        self.assertRaises(ValueError, self.game1.validate_move, 'A5')
        self.assertRaises(ValueError, self.game1.validate_move, 'D2')
        # move to occupied cell
        self.assertRaises(ValueError, self.game2.validate_move, 'c3')

    def test_check_winner(self):
        calling1 = self.game2.check_winner(1, 1)
        self.assertTrue(calling1)
        calling2 = self.game2.check_winner(0, 0)
        self.assertTrue(calling2)
        calling3 = self.game2.check_winner(4, 4)
        self.assertFalse(calling3)

    def test_ai_player(self):
        calling1 = self.game2.ai_player()
        self.assertTrue(calling1 in self.moves_list)


if __name__ == '__main__':
    unittest.main()
