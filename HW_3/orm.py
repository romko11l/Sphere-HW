import sqlite3
import inspect

SQLITE_TYPE_MAP = {
    int: "INTEGER",
    float: "REAL",
    str: "TEXT",
    bool: "INTEGER",  # 0 or 1
}
CREATE_TABLE_SQL = "CREATE TABLE {name} ({fields});"
INSERT_SQL = "INSERT INTO {name} ({fields}) VALUES ({placeholders});"
SELECT_ALL_SQL = "SELECT * FROM {name};"
SELECT_WHERE_SQL = "SELECT * FROM {name} WHERE id=?;"
UPDATE_SQL = "UPDATE {table_name} SET {query} WHERE id=?;"
DELETE_SQL = "DELETE FROM {name} WHERE id=?"


class Database:

    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    def _execute(self, sql, params=None): # дописать тип params
        print(sql, params)
        if params:
            self.conn.execute(sql, params)
        else:
            self.conn.execute(sql)

    def create(self, table):
        self._execute(table._get_create_sql())

    def add(self, instance):
        if instance._id is not None:
            raise ValueError("Этот объект уже занесён в БД")
        instance.__class__._size += 1
        instance._id = instance.__class__._size
        sql, values = instance._get_insert_sql()
        self._execute(sql, values)
        self.conn.commit()

    def all(self, table):
        result = []
        sql = table._get_select_all_sql()
        for row in self.conn.execute(sql):
            result.append(row)
        return result

    def get(self, table, id):
        result = []
        sql = table._get_select_where_sql()
        params = str(id)
        for row in self.conn.execute(sql, params):
            result.append(row)
        return result

    def update(self, instance):
        sql = instance._get_update_sql()
        self._execute(sql, (instance._id,))
        self.conn.commit()

    def delete(self, instance):
        sql = instance._get_delete_sql()
        self._execute(sql, (instance._id,))
        instance._id = None
        self.conn.commit()


class Table:
    _size = 0

    def __init__(self, **kwargs):
        self._id = None
        for name, value in kwargs.items():
            if name in self.__class__.__dict__:
                self.__dict__[name] = value
            else:
                raise ValueError("В таблице нет такого столбца")

    @classmethod
    def _get_name(cls):
        return cls.__name__.lower()

    @classmethod
    def _get_create_sql(cls):
        fields = [
            ("id", "INTEGER PRIMARY KEY AUTOINCREMENT")
        ]
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append((name, field.sql_type))
        fields = [" ".join(x) for x in fields]
        return CREATE_TABLE_SQL.format(name=cls._get_name(),
                                       fields=", ".join(fields))

    def _get_insert_sql(self):
        cls = self.__class__
        fields = []
        placeholders = []
        values = []
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                if isinstance(getattr(self, name), Column):
                    raise ValueError("Не задано значение колонки")
                fields.append(name)
                values.append(getattr(self, name))
                placeholders.append('?')
        sql = INSERT_SQL.format(name=cls._get_name(),
                                fields=", ".join(fields),
                                placeholders=", ".join(placeholders))
        return sql, values

    @classmethod
    def _get_select_all_sql(cls):
        sql = SELECT_ALL_SQL.format(name=cls._get_name())
        return sql

    @classmethod
    def _get_select_where_sql(cls):
        sql = SELECT_WHERE_SQL.format(name=cls._get_name())
        return sql

    def _get_update_sql(self):
        cls = self.__class__
        query = []
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                if isinstance(getattr(self, name), Column):
                    raise ValueError("Не задано значение колонки")
                elif isinstance(getattr(self, name), str):
                    query.append("{name}='{val}'".format(name=name, val=getattr(self, name)))
                else:
                    query.append("{name}={val}".format(name=name, val=getattr(self, name)))
        sql = UPDATE_SQL.format(table_name=self._get_name(),
                                query=", ".join(query))
        return sql

    def _get_delete_sql(self):
        return DELETE_SQL.format(name=self._get_name())

class Column:

    def __init__(self, type): # разобраться как прописать аннотацию type
        self.type = type

    @property
    def sql_type(self):
        return SQLITE_TYPE_MAP[self.type]


if __name__ == '__main__':
    pass
