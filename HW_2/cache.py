from collections import deque


class LRUCache:
    """This structure realize LRU cache."""
    def __init__(self, capacity: int = 10) -> None:
        """Build a cache object.

        Keyword arguments:
            capacity -- cache size

        Exceptions:
            ValueError - if received incorrect capacity
        """
        if capacity < 1:
            raise ValueError
        self._capacity = capacity
        self._hash_table = dict()
        self._deque = deque()

    def get(self, key: str) -> str:
        """Retrieve data from cache by key.

        Keyword arguments:
            key -- data-associated key

        Returns:
            string associated with key
        """
        if key not in self._hash_table:
            return ''
        self._deque.remove(key)
        self._deque.appendleft(key)
        return self._hash_table[key]

    def set(self, key: str, value: str) -> None:
        """Caching data.

        Keyword arguments:
            key -- data-associated key
            value -- cached data
        """
        if key in self._hash_table:
            self._hash_table[key] = value
            self._deque.remove(key)
            self._deque.appendleft(key)
        else:
            if len(self._deque) < self._capacity:
                self._hash_table[key] = value
            else:
                self._hash_table.pop(self._deque.pop())
                self._hash_table[key] = value
            self._deque.appendleft(key)

    def delete(self, key: str) -> None:
        """Deleting data from cache.

        Keyword arguments:
            key -- data-associated key

        Exceptions:
            KeyError - attempt to delete non-existing data
        """
        if key not in self._hash_table:
            raise KeyError
        self._deque.remove(key)
        self._hash_table.pop(key)


if __name__ == '__main__':
    pass
