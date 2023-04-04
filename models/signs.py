from models.sql import *
from models.base import Base


class Signs(Base):
    table_name = 'signs'
    query = \
        ''''
            sign_id INTEGER PRIMARY KEY,
            name varchar(50) NOT NULL
        '''
    create_table(Base.cursor, table_name, query, remove_previous=False)

    @classmethod
    def add_signs(cls, name: str):
        insert_into(cls.cursor, cls.table_name, ['name'], [name])
