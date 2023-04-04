from models.sql import *
from models.base import Base


class History(Base):
    table_name = 'history'
    query = \
        '''
            user_id INTEGER NOT NULL,
            sign_id integer NOT NULL,
            FOREIGN KEY (sign_id) REFERENCES signs (id)
        '''
    create_table(Base.cursor, table_name, query, remove_previous=False)

    @classmethod
    def add_history_note(cls, user_id, sign_id):
        insert_into(cls.cursor, cls.table_name,
                    ['user_id', 'sign_id'], [user_id, sign_id])


