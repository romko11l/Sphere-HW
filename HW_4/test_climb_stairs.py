import unittest
from all_methods import self_written_calc, numpy_calc, slow_calc


class TestCalc(unittest.TestCase):
    def test_self_written_calc(self):
        self.assertEqual(self_written_calc(1), 1)
        self.assertEqual(self_written_calc(2), 2)
        self.assertEqual(self_written_calc(10), 89)
        self.assertEqual(self_written_calc(45), 1836311903)

    def test_numpy_calc(self):
        self.assertEqual(numpy_calc(1), 1)
        self.assertEqual(numpy_calc(2), 2)
        self.assertEqual(numpy_calc(10), 89)
        self.assertEqual(numpy_calc(45), 1836311903)

    def test_slow_calc(self):
        self.assertEqual(slow_calc(1), 1)
        self.assertEqual(slow_calc(2), 2)
        self.assertEqual(slow_calc(10), 89)


if __name__ == '__main__':
    unittest.main()
