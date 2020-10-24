import sqlite3
import inspect

SQLITE_TYPE_MAP = {
    int: "INTEGER",
    float: "REAL",
    str: "TEXT",
    bool: "INTEGER",  # 0 or 1
}
CREATE_TABLE_SQL = "CREATE TABLE {name} ({fields});"


class Database:

    def __init__(self, path : str ) -> None:
        self.conn = sqlite3.connect(path)

    def _execute(self, sql : str, params=None) -> None: # дописать тип params
        if params:
            self.conn.execute(sql, params)
        else:
            self.conn.execute(sql)

    def create(self, table) -> None:
        print(table._get_create_sql())
        self._execute(table._get_create_sql())



class Table:

    @classmethod
    def _get_name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def _get_create_sql(cls) -> str:
        fields = [
            ("id", "INTEGER PRIMARY KEY AUTOINCREMENT")
        ]

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append((name, field.sql_type))
            elif isinstance(field, ForeignKey):
                fields.append((name + "_id", "INTEGER"))

        fields = [" ".join(x) for x in fields]
        return CREATE_TABLE_SQL.format(name=cls._get_name(),
                                       fields=", ".join(fields))

class Column:

    def __init__(self, type) -> None: # разобраться как прописать аннотацию type
        self.type = type

    @property
    def sql_type(self) -> str:
        return SQLITE_TYPE_MAP[self.type]

class ForeignKey:

    def __init__(self, table) -> None:
        self.table = table

if __name__ == '__main__':
    pass
