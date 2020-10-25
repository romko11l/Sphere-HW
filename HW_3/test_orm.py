import os
from orm import Database
from orm import Table, Column

DB_PATH = "./test.db"

class Author(Table):
    name = Column(str)
    lucky_number = Column(int)

if __name__ == '__main__':
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    db = Database(DB_PATH)
    db.create(Author)

    greg = Author()
    greg.name = 'greg'
    greg.lucky_number = 12
    roma = Author()
    roma.name = 'roma'
    roma.lucky_number = 17
    db.add(greg)
    db.add(roma)
    print(db.all(Author))
    greg.lucky_number = 13
    db.update(greg)
    print(db.all(Author))
