from orm import Database
from orm import Table, Column, ForeignKey

DB_PATH = "./test.db"

class Author(Table):
    name = Column(str)
    lucky_number = Column(int)

class Post(Table):
    title = Column(str)
    published = Column(bool)
    author = ForeignKey(Author)

if __name__ == '__main__':
    db = Database(DB_PATH)
    db.create(Author)
    db.create(Post)
