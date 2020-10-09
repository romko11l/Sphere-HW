import unittest
from cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def setUp(self):
        self.cache1 = LRUCache(100)
        self.cache2 = LRUCache(1)
        self.cache3 = LRUCache(2)
        self.cache4 = LRUCache(1)
        self.cache5 = LRUCache(2)

    def test_init(self):
        self.assertRaises(ValueError, LRUCache, 0)
        self.assertRaises(ValueError, LRUCache, -100)

    def test_get(self):
        self.cache2.set('1', '1')
        self.assertEqual(self.cache2.get('1'), '1')
        self.cache2.set('2', '2')
        self.assertEqual(self.cache2.get('1'), '')
        self.assertEqual(self.cache2.get('2'), '2')

        self.cache3.set('1', '1')
        self.cache3.set('2', '2')
        self.assertEqual(self.cache3.get('1'), '1')
        self.cache3.set('3', '3')
        self.assertEqual(self.cache3.get('1'), '1')
        self.assertEqual(self.cache3.get('2'), '')

    def test_set(self):
        self.cache4.set('1', '1')
        self.assertEqual(self.cache4.get('1'), '1')

    def test_delete(self):
        self.cache5.set('1', '1')
        self.cache5.set('2', '2')
        self.cache5.delete('1')
        self.assertEqual(self.cache5.get('1'), '')
        self.assertEqual(self.cache5.get('2'), '2')
        self.assertRaises(KeyError, self.cache5.delete, '1')
        self.assertRaises(KeyError, self.cache5.delete, '3')

    def test_from_task(self):
        self.cache1.set('Jesse', 'Pinkman')
        self.cache1.set('Walter', 'White')
        self.cache1.set('Jesse', 'James')
        self.assertEqual(self.cache1.get('Jesse'), 'James')
        self.cache1.delete('Walter')
        self.assertEqual(self.cache1.get('Walter'), '')

if __name__ == '__main__':
    unittest.main()
