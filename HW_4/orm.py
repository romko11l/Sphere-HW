"""Реализация ORM, работающей с sqlite3"""
import sqlite3
import inspect
import logging
from datetime import datetime

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

CREATE_TABLE = "%s: Создана таблица %s"
INSERT_RECORD = "%s: В таблицу %s добавлена запись с id=%s"
UPDATE_RECORD = "%s: В таблице %s обновлена запись с id=%s"
DELETE_RECORD = "%s: Из таблицы %s удалена запись с id=%s"
GET_RECORD = "%s: Из таблицы %s запрошена запись с id=%s"
ALL_RECORDS = "%s: Из таблицы %s запрошены все записи"

TABLE_INIT_ERROR = "%s: Попытка создать невалидный объект типа %s"
INSERT_ERROR = "%s: Попытка записи в таблицу %s невалидного объекта"
UPDATE_ERROR = "%s: Попытка обновить запись в таблице %s невалидным объектом"


class Database:
    """Класс, поддерживающий основные (CRUD) операции с БД"""
    def __init__(self, path):
        """Инициализация соединения с БД

        Keyword arguments:
            path -- путь к БД
        """
        logging.basicConfig(filename="orm.log", level=logging.INFO)
        self.conn = sqlite3.connect(path)

    def _execute(self, sql, params=None):
        """Внутренний метод исполнения sql запроса

        Keyword arguments:
            sql -- SQL запрос (возможно, в нём будут '?')
            params -- параметры, замещающие '?' в sql
        """
        if params:
            self.conn.execute(sql, params)
        else:
            self.conn.execute(sql)

    def create(self, table):
        """Метод создания таблицы

        Keyword arguments:
            table -- класс-таблица
        """
        self._execute(table.get_create_sql())
        logging.info(CREATE_TABLE, datetime.today(), table.get_name())

    def add(self, instance):
        """Метод вставки объекта-строки таблицы в БД

        Keyword arguments:
            instance -- объект-строка таблицы instance.__class__

        Exceptions:
            ValueError - если объект уже занесён в БД
        """
        if instance.record_id is not None:
            raise ValueError("Этот объект уже занесён в БД")
        sql, values = instance.get_insert_sql()
        self._execute(sql, values)
        instance.__class__.size_inc()
        instance.record_id = instance.__class__.size()
        self.conn.commit()
        logging.info(INSERT_RECORD, datetime.today(), instance.get_name(),
                     instance.record_id)

    def all(self, table):
        """Запрос на вывод содержимого таблицы

        Keyword arguments:
            table -- класс-таблица

        Returns:
            содержимое таблицы в виде списка кортежей
        """
        result = []
        sql = table.get_select_all_sql()
        for row in self.conn.execute(sql):
            result.append(row)
        logging.info(ALL_RECORDS, datetime.today(), table.get_name())
        return result

    def get(self, table, record_id):
        """Запрос на вывод содержимого таблицы по id

        Keyword arguments:
            table -- класс-таблица
            record_id -- id записи в таблице table

        Returns:
            содержимое таблицы по id=record_id
        """
        result = []
        sql = table.get_select_where_sql()
        params = (str(record_id),)
        for row in self.conn.execute(sql, params):
            result.append(row)
        logging.info(GET_RECORD, datetime.today(), table.get_name(),
                     record_id)
        return result

    def update(self, instance):
        """Запрос на обновление строки таблицы, соответствующей instance

        Keyword arguments:
            instance -- объект-строка таблицы instance.__class__
        """
        sql = instance.get_update_sql()
        self._execute(sql, (str(instance.record_id),))
        self.conn.commit()
        logging.info(UPDATE_RECORD, datetime.today(), instance.get_name(),
                     instance.record_id)

    def delete(self, instance):
        """Запрос на удаление строки таблицы, соответствующей instance

        Keyword arguments:
            instance -- объект-строка таблицы instance.__class__
        """
        sql = instance.get_delete_sql()
        self._execute(sql, (str(instance.record_id),))
        self.conn.commit()
        logging.info(DELETE_RECORD, datetime.today(), instance.get_name(),
                     instance.record_id)
        instance.record_id = None

    def __del__(self):
        """Закрытие соединения с БД"""
        self.conn.close()


class Table:
    """Класс для работы с конкретной таблицей БД"""
    _size = 0

    def __init__(self, **kwargs):
        """Инициализация объекта-строки

        Keyword arguments:
            kwargs -- значения в колонке таблицы

        Exceptions:
            ValueError - в таблице нет одной из указанных колонок
        """
        self.record_id = None
        for name, value in kwargs.items():
            if name in self.__class__.__dict__:
                self.__dict__[name] = value
            else:
                logging.error(TABLE_INIT_ERROR, datetime.today(),
                              self.get_name())
                raise ValueError("В таблице нет такой колонки")

    @property
    def record_id(self):
        """Getter record_id"""
        return self._id

    @record_id.setter
    def record_id(self, new_id):
        """Setter record_id"""
        self._id = new_id

    @classmethod
    def size(cls):
        """
        Returns:
            Текущий размер таблицы (номер последнего id в ней)
        """
        return cls._size

    @classmethod
    def size_inc(cls):
        """Инкрементирует хранимый размер таблицы"""
        cls._size += 1

    @classmethod
    def set_size(cls, new_size):
        """Задание текущего размера таблицы
        (нужно для операций с заранее заданной таблицей)

        Keyword arguments:
            new_size -- новый размер таблицы
        """
        cls._size = new_size

    @classmethod
    def size_zeroing(cls):
        """Обнуляет число элементов таблицы (нужно при тестировании)"""
        cls._size = 0

    @classmethod
    def get_name(cls):
        """
        Returns:
            название таблицы в БД
        """
        return cls.__name__.lower()

    @classmethod
    def get_create_sql(cls):
        """Создание запроса на создание таблицы БД

        Returns:
            Сгенерированный запрос
        """
        fields = [
            ("id", "INTEGER PRIMARY KEY AUTOINCREMENT")
        ]
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append((name, field.sql_type))
        fields = [" ".join(x) for x in fields]
        return CREATE_TABLE_SQL.format(name=cls.get_name(),
                                       fields=", ".join(fields))

    def get_insert_sql(self):
        """Создание запроса на вставку строки в таблицу

        Returns:
            Кортеж из запроса с '?' на месте значений и самих значений
        """
        cls = self.__class__
        fields = []
        placeholders = []
        values = []
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                if isinstance(getattr(self, name), Column):
                    logging.error(INSERT_ERROR, datetime.today(),
                                  self.get_name())
                    raise ValueError("Не задано значение колонки")
                fields.append(name)
                values.append(getattr(self, name))
                placeholders.append('?')
        sql = INSERT_SQL.format(name=cls.get_name(),
                                fields=", ".join(fields),
                                placeholders=", ".join(placeholders))
        return sql, values

    @classmethod
    def get_select_all_sql(cls):
        """
        Returns:
            Запрос на вывод всего содержимого таблицы
        """
        sql = SELECT_ALL_SQL.format(name=cls.get_name())
        return sql

    @classmethod
    def get_select_where_sql(cls):
        """
        Returns:
            Запрос на вывод строки таблицы по id с '?' вместо id
        """
        sql = SELECT_WHERE_SQL.format(name=cls.get_name())
        return sql

    def get_update_sql(self):
        """Создание запроса на изменение строки в таблице

        Returns:
            Запрос-UPDATE с '?' вместо id
        """
        cls = self.__class__
        query = []
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                if isinstance(getattr(self, name), Column):
                    logging.error(UPDATE_ERROR, datetime.today(),
                                  self.get_name())
                    raise ValueError("Не задано значение колонки")
                val = getattr(self, name)
                if isinstance(getattr(self, name), str):
                    query.append("{name}='{val}'".format(name=name, val=val))
                else:
                    query.append("{name}={val}".format(name=name, val=val))
        sql = UPDATE_SQL.format(table_name=self.get_name(),
                                query=", ".join(query))
        return sql

    def get_delete_sql(self):
        """
        Returns:
            Запрос на удаление строки таблицы по id с '?' вместо id
        """
        return DELETE_SQL.format(name=self.get_name())


class Column:
    """Класс для отображения типов python в SQL типы"""
    def __init__(self, column_type):
        """Инициализация объекта-типа столбца таблицы

        Keyword arguments:
            column_type -- один из классов int, float, str, bool

        Returns:
            Запрос-UPDATE с '?' вместо id
        """
        self._type = column_type

    @property
    def sql_type(self):
        """Getter для SQL типа, заданного объектом этого класса"""
        return SQLITE_TYPE_MAP[self._type]


if __name__ == '__main__':
    pass
