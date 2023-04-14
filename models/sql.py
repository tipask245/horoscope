import sqlite3

DB_PATH = 'horoscope.sqlite'


def connect_db():
    """Подключение к бд по path"""
    try:
        db = sqlite3.connect(DB_PATH)
        cursor = db.cursor()
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


def insert_into(table_name: str, columns: list | tuple, values: list | tuple):
    """Вставка полученных значений по колонкам"""
    text = \
        f'''
            INSERT INTO {table_name} ({", ".join(columns)})
            VALUES ({', '.join(['"' + str(value) + '"' for value in values])})
        '''
    return execute_query(text)


def delete_from(table_name: str, condition=None):
    """Удаление строки, условие опционально"""
    if not condition:
        return execute_query(f'DELETE FROM {table_name}')
    text = f'DELETE FROM {table_name} WHERE {condition}'
    return execute_query(text)


def select_one(table_name: str, columns: list | tuple, condition: None | str = None) -> tuple | None:
    """Получение одной записи из бд по колонкам и условию (опционально)"""
    db, cursor = connect_db()
    if not condition:
        result = cursor.execute(f'SELECT {", ".join(columns)} FROM {table_name}').fetchone()
        db.close()
        return result
    text = f'SELECT {", ".join(columns)} FROM {table_name} WHERE {condition}'
    result = cursor.execute(text).fetchone()
    db.close()
    return result


def select_all(table_name: str, columns: list | tuple, condition: None | str = None) -> list:
    """Получение всех записей из бд по колонкам и условию (опционально)"""
    db, cursor = connect_db()
    text = f'SELECT {", ".join(columns)} FROM {table_name} WHERE {condition}'
    if not condition:
        text = f'SELECT {", ".join(columns)} FROM {table_name}'
    result = cursor.execute(text).fetchall()
    db.close()
    return result


def custom_select_all_by_query(query: str) -> list:
    """Получение всех записей из бд по кастомному запросу"""
    db, cursor = connect_db()
    result = cursor.execute(query).fetchall()
    db.close()
    return result


def create_table(table_name: str, query: str, remove_previous: bool = False):
    """Создание таблицы из имени и текста запроса"""
    if remove_previous:
        execute_query(f'DROP TABLE IF EXISTS {table_name}')
    return execute_query(f'CREATE TABLE IF NOT EXISTS {table_name} ({query})')
