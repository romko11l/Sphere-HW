"""Тесты для orm.py"""
import unittest
import os
import sqlite3
from orm import Database, Table, Column

DB_PATH = "./test.db"


class Author(Table):
    name = Column(str)
    surname = Column(str)


class Book(Table):
    ISBN = Column(str)
    in_stock = Column(bool)
    cost = Column(float)
    author_id = Column(int)


class TestColumn(unittest.TestCase):
    def test_sql_type(self):
        col1 = Column(int)
        col2 = Column(str)
        col3 = Column(bool)
        col4 = Column(float)

        self.assertEqual(col1.sql_type, 'INTEGER')
        self.assertEqual(col2.sql_type, 'TEXT')
        self.assertEqual(col3.sql_type, 'INTEGER')
        self.assertEqual(col4.sql_type, 'REAL')


class TestTable(unittest.TestCase):
    def test_init(self):
        tolstoy = Author(name='Lev', surname='Tolstoy')
        pushkin = Author(name='Alexander')
        bulgakov = Author(surname='Bulgakov')

        self.assertEqual(tolstoy.name, 'Lev')
        self.assertEqual(tolstoy.surname, 'Tolstoy')
        self.assertEqual(pushkin.name, 'Alexander')
        self.assertEqual(bulgakov.surname, 'Bulgakov')

        self.assertRaises(ValueError, Author, year=2099)

    def test_get_name(self):
        tolstoy = Author()
        anna_karenina = Book()

        self.assertEqual(tolstoy.get_name(), 'author')
        self.assertEqual(anna_karenina.get_name(), 'book')
        self.assertEqual(Author.get_name(), 'author')

    def test_get_create_sql(self):
        res1 = 'CREATE TABLE author (id INTEGER PRIMARY KEY AUTOINCREMENT, \
name TEXT, surname TEXT);'
        res2 = 'CREATE TABLE book (id INTEGER PRIMARY KEY AUTOINCREMENT, \
ISBN TEXT, author_id INTEGER, cost REAL, in_stock INTEGER);'

        self.assertEqual(Author.get_create_sql(), res1)
        self.assertEqual(Book.get_create_sql(), res2)

    def test_get_insert_sql(self):
        tolstoy = Author(name='Lev', surname='Tolstoy')
        pushkin = Author(name='Alexander')
        res1 = ('INSERT INTO author (name, surname) VALUES (?, ?);',
                ['Lev', 'Tolstoy'])

        self.assertEqual(tolstoy.get_insert_sql(), res1)

        self.assertRaises(ValueError, pushkin.get_insert_sql)

    def test_get_select_all_sql(self):
        res1 = 'SELECT * FROM author;'
        res2 = 'SELECT * FROM book;'

        self.assertEqual(Author.get_select_all_sql(), res1)
        self.assertEqual(Book.get_select_all_sql(), res2)

    def test_get_select_where_sql(self):
        res1 = 'SELECT * FROM author WHERE id=?;'
        res2 = 'SELECT * FROM book WHERE id=?;'

        self.assertEqual(Author.get_select_where_sql(), res1)
        self.assertEqual(Book.get_select_where_sql(), res2)

    def test_get_update_sql(self):
        tolstoy = Author(name='Lev', surname='Tolstoy')
        pushkin = Author(name='Alexander')
        res1 = "UPDATE author SET name='Lev', surname='Tolstoy' WHERE id=?;"

        self.assertEqual(tolstoy.get_update_sql(), res1)

        self.assertRaises(ValueError, pushkin.get_update_sql)

    def test_get_delete_sql(self):
        tolstoy = Author(name='Lev', surname='Tolstoy')
        res1 = 'DELETE FROM author WHERE id=?'

        self.assertEqual(tolstoy.get_delete_sql(), res1)


class TestDatabase(unittest.TestCase):
    def test_create(self):
        Author.size_zeroing()
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        db = Database(DB_PATH)
        db.create(Author)

        self.assertIsInstance(db.conn.execute('SELECT * FROM author'),
                              sqlite3.Cursor)

        self.assertRaises(sqlite3.OperationalError, db.conn.execute,
                          'SELECT * FROM book')

    def test_add(self):
        Author.size_zeroing()
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        db = Database(DB_PATH)
        db.create(Author)
        tolstoy = Author(name='Lev', surname='Tolstoy')
        pushkin = Author(name='Alexander')

        self.assertRaises(ValueError, db.add, pushkin)

        pushkin.surname = 'Pushkin'
        db.add(tolstoy)
        db.add(pushkin)
        res1 = [(1, 'Lev', 'Tolstoy'), (2, 'Alexander', 'Pushkin')]

        self.assertEqual(db.all(Author), res1)

        self.assertRaises(ValueError, db.add, tolstoy)

    def test_all(self):
        Author.size_zeroing()
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        db = Database(DB_PATH)
        db.create(Author)
        tolstoy = Author(name='Lev', surname='Tolstoy')
        pushkin = Author(name='Alexander', surname='Pushkin')
        db.add(tolstoy)

        self.assertEqual(db.all(Author), [(1, 'Lev', 'Tolstoy')])

        db.add(pushkin)
        res1 = [(1, 'Lev', 'Tolstoy'), (2, 'Alexander', 'Pushkin')]

        self.assertEqual(db.all(Author), res1)

    def test_get(self):
        Author.size_zeroing()
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        db = Database(DB_PATH)
        db.create(Author)
        tolstoy = Author(name='Lev', surname='Tolstoy')
        pushkin = Author(name='Alexander', surname='Pushkin')
        db.add(tolstoy)
        db.add(pushkin)

        self.assertEqual(db.get(Author, 2), [(2, 'Alexander', 'Pushkin')])
        self.assertEqual(db.get(Author, 3), [])
        self.assertEqual(db.get(Author, 100), [])
        self.assertEqual(db.get(Author, -1), [])

    def test_update(self):
        Author.size_zeroing()
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        db = Database(DB_PATH)
        db.create(Author)
        tolstoy = Author(name='Lev', surname='Tolstoy')
        pushkin = Author(name='Alexander', surname='Pushkin')
        db.add(tolstoy)
        db.add(pushkin)
        tolstoy.name = 'Aleksey'
        db.update(tolstoy)
        res1 = [(1, 'Aleksey', 'Tolstoy'), (2, 'Alexander', 'Pushkin')]

        self.assertEqual(db.all(Author), res1)

    def test_delete(self):
        Author.size_zeroing()
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        db = Database(DB_PATH)
        db.create(Author)
        tolstoy = Author(name='Lev', surname='Tolstoy')
        pushkin = Author(name='Alexander', surname='Pushkin')
        db.add(tolstoy)
        db.add(pushkin)
        db.delete(tolstoy)

        self.assertEqual(db.all(Author), [(2, 'Alexander', 'Pushkin')])

        db.add(tolstoy)
        res1 = [(2, 'Alexander', 'Pushkin'), (3, 'Lev', 'Tolstoy')]

        self.assertEqual(db.all(Author), res1)


if __name__ == '__main__':
    unittest.main()
