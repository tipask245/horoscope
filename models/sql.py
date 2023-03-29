import sqlite3

DB_PATH = 'horoscope.sqlite'


def connect_db(db_path):
    """Подключение к бд по path"""
    try:
        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        print(f'connect to {db_path}')
    except Exception as err:
        print(f'Ошибка подключения: {type(err)}, {err}')
        return []
    return db, cursor


def execute_query(cursor: sqlite3.Cursor, full_query: str):
    """"Выполнение любого запроса"""
    cursor.execute(full_query)


def create_table(cursor: sqlite3.Cursor, table_name: str, query: str, remove_previous=False):
    """Создание таблицы из имени таблицы и текста запроса"""
    try:
        if remove_previous:
            cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
        cursor.execute(f'CREATE TABLE IF NOT EXIST {table_name} ({query})')
    except Exception as err:
        print(f'Есть ошибка: {type(err)} => {err}')
