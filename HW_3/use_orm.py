import os
from orm import Database, Table, Column

DB_PATH = "./test.db"

class Author(Table):
    name = Column(str)
    lucky_number = Column(int)

if __name__ == '__main__':
    """
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    """
    db = Database(DB_PATH)
    #db.create(Author)
    """
    greg = Author()
    greg.name = 'greg'
    greg.lucky_number = 12
    greg.mem = 3
    """
    Author._size = len(db.all(Author))
    print(Author.size())
    print(db.all(Author))
