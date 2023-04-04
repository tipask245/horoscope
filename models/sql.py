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
    try:
        cursor.execute(full_query)
    except Exception as err:
        print(f'Ошибка: {type(err)} => {err}')


def create_table(cursor: sqlite3.Cursor, table_name: str, query: str, remove_previous=False):
    """Создание таблицы из имени таблицы и текста запроса"""
    if remove_previous:
        execute_query(cursor, f'DROP TABLE IF EXISTS {table_name}')
    execute_query(cursor, f'CREATE TABLE IF NOT EXIST {table_name} ({query})')


def insert_into(cursor: sqlite3.Cursor, table_name, columns: list | tuple, values: list | tuple):
    text = \
        f'''
            INSERT INTO {table_name} ({", ".join(columns)})
            VALUES ({', '.join(['"' + str(value) + '"' for value in values])})
        '''
    execute_query(cursor, text)


def delete_from(cursor: sqlite3.Cursor, table_name, condition=None):
    if not condition:
        return execute_query(cursor, f'DELETE FROM {table_name}')
    text = \
        f'''
            DELETE FROM {table_name}
            WHERE {condition}
        '''
    execute_query(cursor, text)
