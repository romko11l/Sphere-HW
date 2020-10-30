import os
from orm import Database, Table, Column

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

    roman = Author(name='roma', lucky_number=17)

    alice = Author(name='alice', lucky_number=-1)

    db.add(roman)
    db.add(alice)
    db.add(greg)

    print(db.all(Author))

    alice.lucky_number = 10

    db.update(alice)

    print(db.all(Author))

    db.delete(alice)

    print(db.all(Author))

    print(db.get(Author, 2))

    print(db.get(Author, 3))

    db.add(alice)

    print(db.all(Author))
