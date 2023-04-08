import json
from models.sql import *


class Sign:
    table_name = 'signs'
    query = \
        '''
            sign_id INTEGER PRIMARY KEY,
            name varchar(50) NOT NULL,
            translated_name varchar(50) NOT NULL
        '''
    create_table(table_name, query, remove_previous=False)

    @classmethod
    def add_signs(cls, sign_id: int, name: str, translated_name: str):
        insert_into(cls.table_name, ['sign_id', 'name', 'translated_name'], [sign_id, name, translated_name])

    @classmethod
    def add_all_signs_from_json(cls):
        with open(f'{cls.table_name}.json', 'r', encoding='utf-8') as file:
            parsed_signs = json.load(file)
            for sign in parsed_signs:
                cls.add_signs(sign['sign_id'], sign['name'], sign['translated_name'])
