from models.sql import *


class History:
    table_name = 'history'
    query = \
        '''
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            sign_id INTEGER NOT NULL,
            FOREIGN KEY (sign_id) REFERENCES signs (id)
        '''
    create_table(table_name, query, remove_previous=False)

    @classmethod
    def get_notes_by_user_id(cls, user_id: int):
        columns = ['signs.id', 'signs.name', 'signs.translated_name', 'signs.horoscope_type']
        on_condition = 'history.sign_id = signs.id'
        condition = f'history.user_id = {user_id}'
        query = f'SELECT {", ".join(columns)} FROM {cls.table_name} INNER JOIN signs ON {on_condition} WHERE {condition}'
        return custom_select_all_by_query(query=query)[::-1]

    @classmethod
    def add_history_note(cls, user_id: int, sign_name: str):
        count = len(select_all(table_name=cls.table_name, columns=['*'], condition=f'user_id = {user_id}'))
        sign_id = select_one('signs', columns=['id'], condition=f'name = "{sign_name}"')[0]
        existed_note = select_one(table_name=cls.table_name, columns=['id'],
                                  condition=f'user_id = {user_id} AND sign_id = {sign_id}')
        if existed_note:
            delete_from(table_name=cls.table_name, condition=f'id = {existed_note[0]}')
        if count == 5:
            condition = f'id = (SELECT MIN(id) FROM {cls.table_name} WHERE user_id = {user_id})'
            delete_from(table_name=cls.table_name, condition=condition)
        insert_into(table_name=cls.table_name, columns=['user_id', 'sign_id'],
                    values=[user_id, sign_id])


