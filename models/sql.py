import sqlite3

DB_PATH = 'horoscope.sqlite'


def connect_db():
    """Подключение к бд по path"""
    try:
        db = sqlite3.connect(DB_PATH)
        cursor = db.cursor()
        print(f'connect to {DB_PATH}')
    except Exception as err:
        print(f'Ошибка подключения: {type(err)}, {err}')
        return []
    return db, cursor


def execute_query(full_query: str):
    """"Выполнение любого запроса"""
    try:
        db, cursor = connect_db()
        cursor.execute(full_query)
        db.commit()
        db.close()
    except Exception as err:
        print(f'Ошибка: {type(err)} => {err}')


def insert_into(table_name, columns: list | tuple, values: list | tuple):
    text = \
        f'''
            INSERT INTO {table_name} ({", ".join(columns)})
            VALUES ({', '.join(['"' + str(value) + '"' for value in values])})
        '''
    execute_query(text)


def delete_from(table_name, condition=None):
    if not condition:
        return execute_query(f'DELETE FROM {table_name}')
    text = \
        f'''
            DELETE FROM {table_name}
            WHERE {condition}
        '''
    execute_query(text)


def create_table(table_name: str, query: str, remove_previous=False):
    """Создание таблицы из имени таблицы и текста запроса"""
    if remove_previous:
        execute_query(f'DROP TABLE IF EXISTS {table_name}')
    execute_query(f'CREATE TABLE IF NOT EXISTS {table_name} ({query})')
