from models.sql import *


class History:
    table_name = 'history'
    query = \
        '''
            user_id INTEGER NOT NULL,
            sign_id integer NOT NULL,
            FOREIGN KEY (sign_id) REFERENCES signs (id)
        '''
    create_table(table_name, query, remove_previous=False)

    @classmethod
    def add_history_note(cls, user_id, sign_id):
        insert_into(cls.table_name,
                    ['user_id', 'sign_id'], [user_id, sign_id])


