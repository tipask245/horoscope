import json
from models.sql import *


class Sign:
    table_name = 'signs'
    query = \
        '''
            id INTEGER PRIMARY KEY,
            sign_num INTEGER,
            name varchar(50) NOT NULL,
            translated_name varchar(50) NOT NULL,
            horoscope_type varchar(50) NOT NULL
        '''
    create_table(table_name, query, remove_previous=False)

    @classmethod
    def add_sign(cls, sign_id: int, name: str, translated_name: str, horoscope_type: str):
        insert_into(cls.table_name, ['sign_num', 'name', 'translated_name', 'horoscope_type'],
                    [sign_id, name, translated_name, horoscope_type])

    @classmethod
    def add_all_signs_from_json(cls):
        with open(f'{cls.table_name}.json', 'r', encoding='utf-8') as file:
            parsed_signs = json.load(file)
            for sign in parsed_signs:
                cls.add_sign(sign['sign_num'], sign['name'], sign['translated_name'], sign['horoscope_type'])

    @classmethod
    def get_sign_by_translated_name(cls, translated_name: str):
        sign = select_one(table_name=cls.table_name, columns=['sign_num', 'name', 'translated_name', 'horoscope_type'],
                          condition=f'translated_name LIKE "%{translated_name.capitalize()}%"')
        return sign
