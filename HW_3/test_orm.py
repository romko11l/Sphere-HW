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

        self.assertEqual(tolstoy._get_name(), 'author')
        self.assertEqual(anna_karenina._get_name(), 'book')
        self.assertEqual(Author._get_name(), 'author')

    def test_get_create_sql(self):
        res1 = 'CREATE TABLE author (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT);'
        res2 = 'CREATE TABLE book (id INTEGER PRIMARY KEY AUTOINCREMENT, ISBN TEXT, author_id INTEGER, cost REAL, in_stock INTEGER);'

        self.assertEqual(Author._get_create_sql(), res1)
        self.assertEqual(Book._get_create_sql(), res2)

    def test_get_insert_sql(self):
        tolstoy = Author(name='Lev', surname='Tolstoy')
        pushkin = Author(name='Alexander')
        res1=('INSERT INTO author (name, surname) VALUES (?, ?);',
             ['Lev', 'Tolstoy'])

        self.assertEqual(tolstoy._get_insert_sql(), res1)

        self.assertRaises(ValueError, pushkin._get_insert_sql)

    def test_get_select_all_sql(self):
        res1 = 'SELECT * FROM author;'
        res2 = 'SELECT * FROM book;'

        self.assertEqual(Author._get_select_all_sql(), res1)
        self.assertEqual(Book._get_select_all_sql(), res2)

    def test_get_select_where_sql(self):
        res1 = 'SELECT * FROM author WHERE id=?;'
        res2 = 'SELECT * FROM book WHERE id=?;'

        self.assertEqual(Author._get_select_where_sql(), res1)
        self.assertEqual(Book._get_select_where_sql(), res2)

    def test_get_update_sql(self):
        tolstoy = Author(name='Lev', surname='Tolstoy')
        pushkin = Author(name='Alexander')
        res1 = "UPDATE author SET name='Lev', surname='Tolstoy' WHERE id=?;"

        self.assertEqual(tolstoy._get_update_sql(), res1)

        self.assertRaises(ValueError, pushkin._get_update_sql)

    def test_get_delete_sql(self):
        tolstoy = Author(name='Lev', surname='Tolstoy')
        res1 = 'DELETE FROM author WHERE id=?'

        self.assertEqual(tolstoy._get_delete_sql(), res1)

if __name__ == '__main__':
    unittest.main()
