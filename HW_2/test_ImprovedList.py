"""Test for ImprovedList.py"""
import unittest
from ImprovedList import ImprovedList


class TestImprovedList(unittest.TestCase):
    def test_arithmetic(self):
        list1 = ImprovedList([1, 2, 3])
        list2 = ImprovedList([4, 5, 6])
        list3 = ImprovedList([10])
        list4 = ImprovedList()

        self.assertEqual(list1 + list2, ImprovedList([5, 7, 9]))
        self.assertEqual(list1 + list3, ImprovedList([11, 2, 3]))
        self.assertEqual(list3 + list4, ImprovedList([10]))

        self.assertEqual(list1 - list3, ImprovedList([-9, 2, 3]))
        self.assertEqual(list4 - list3, ImprovedList([-10]))

        self.assertEqual(+list1, ImprovedList([1, 2, 3]))

        self.assertEqual(-list1, ImprovedList([-1, -2, -3]))

        list1 += list2
        list3 += list2

        self.assertEqual(list1, ImprovedList([5, 7, 9]))
        self.assertEqual(list3, ImprovedList([14, 5, 6]))

        list4 -= list2

        self.assertEqual(list4, ImprovedList([-4, -5, -6]))

    def test_comparison(self):
        list1 = ImprovedList([1, 2, 3])
        list2 = ImprovedList([4, 5, 6])
        list3 = ImprovedList([6])
        list4 = ImprovedList()

        self.assertGreater(list1, list4)
        self.assertGreaterEqual(list1, list3)
        self.assertLess(list1, list2)
        self.assertLessEqual(list1, list3)
        self.assertEqual(list1, list3)
        self.assertNotEqual(list3, list4)


if __name__ == '__main__':
    unittest.main()
